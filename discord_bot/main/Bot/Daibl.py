import asyncio
import os
import threading
import time
import traceback
import wave
import discord
from discord.ext import commands
import torch
import whisper

from util.Antiblocking import run_blocking
from util.AudioResample import resample_and_save, resample_alt
from LLM.ModelCommunicator import ModelCommunicator
from TTS_Bot.DaiblVoice import Voice
from STT.Hotword.detection import hw_detection
from STT.LiveTranscripe import LiveTranscription
from scrap.query_crafter import  get_query_embeddings_MiniLM, get_query_TF_IDF
from util.Environment import add_path, find_binary


class Daibl(commands.Bot):
    """
    Bot is only responsible for Discord events/commands

    ...

    Attributes
    ----------
    command_prefix : str
        command prefix the bot listens to
    guild_id : int
        server bot is assigned to
    """

    def __init__(
        self,
        command_prefix: str,
        self_bot: bool,
        guild_id: int,
        modelCommunicator: ModelCommunicator,
        voice: Voice,
        PROJECT_PATH: str,
    ):
        commands.Bot.__init__(
            self,
            command_prefix=command_prefix,
            intents=discord.Intents.all(),
            self_bot=self_bot,
        )
        self.PROJECT_PATH = PROJECT_PATH
        self.guild_id = guild_id
        self.modelCommunicator = modelCommunicator
        self.voice = voice
        self.stt : whisper.Whisper = whisper.load_model('medium').to('cuda')

        self.vc = None
        self.audio_data = None
        self.audio_thread = None
        self.transcription = ""
        self.audio_input = os.path.join(PROJECT_PATH, "discord_bot/main/STT/input.wav")
        self.add_bot_commands()

    async def on_ready(self):
        """start up routine"""
        # bot_test channel is referenced
        channel = self.get_channel(1086951624381059112)

        # get the guild
        guild = self.get_guild(self.guild_id)
        # console output
        print(
            f"\n[INFO]: Daibl now online:"
            f"\n{self.user} is connected to the following guild:\n"
            f"{guild.name} (id: {guild.id})\n"
            f"{self.user} will post messages to channel:{channel.name}\n"
        )
        # bot is ready message
        await channel.send("hi im daibl. At your service", tts=True)

    async def on_message(self, message):
        """processing of channel messages"""
        # checks message in every channel
        if message.author == self.user:
            return

        # all infos of message (channel, author, ...)
        print()
        print(message)
        print()

        await self.process_commands(message)
    
    # audio processing
    def pull_audio(self, voice_client : discord.VoiceClient, id):
        while voice_client.recording:
            time.sleep(0.5)
            sink_data = voice_client.sink.audio_data.items()
            try:
                for user_id, data in sink_data:
                    if id == user_id:
                        self.audio_data = data.file
                        self.audio_data.seek(0)
                        with wave.open(self.audio_input, "wb") as f:
                            f.setnchannels(voice_client.decoder.CHANNELS)
                            f.setsampwidth(voice_client.decoder.SAMPLE_SIZE // voice_client.decoder.CHANNELS)
                            f.setframerate(voice_client.decoder.SAMPLING_RATE)
                            f.writeframes(self.audio_data.read())
                        
                print("\nStill processing/pulling audio from discord... ", voice_client.recording)
            except Exception as e:
                traceback.print_exc()
                print(e)
                continue
        

    def add_bot_commands(self):
        """any commands the bot listens to when the prefix is used"""

        @self.command(name="status", pass_context=True)
        async def status(ctx: commands.Context):
            """greeting author"""
            print(ctx)
            await ctx.channel.send("Hello" + " " + ctx.author.name)

        @self.command(name="join", pass_context=True)
        async def join(ctx: commands.Context):
            """join voice channel"""
            try:
                self.vc = await ctx.author.voice.channel.connect()
            except Exception as e:
                print(e)
                await self.vc.disconnect()
                pass

        @self.command(name="dc", pass_context=True)
        async def disconnect(ctx: commands.Context):
            """disconnect voice channel"""
            try:
                await self.vc.disconnect()
            except Exception as e:
                print(e)
                pass

        @self.command(name="daibl", pass_context=True)
        async def adress_bot(ctx: commands.Context):
            """communicate with LLM module"""
            #query = get_query_embeddings_MiniLM(ctx.message.content.replace("$daibl ", ""))
            
            # if "$daibl" in ctx.message.content:
            #     prombt = ctx.message.content.replace("$daibl ", "")
            # else:
            #     prombt = ctx.message.content
            prompt = await run_blocking(get_query_TF_IDF, self, ctx.message.content.replace("$daibl ", ""))
            answer = await run_blocking(self.modelCommunicator.returnPromptText, self, prompt)
            # answer = answer[-100:]
            answer = answer[:1900]
            await ctx.channel.send(answer)
            self.vc = await self.voice.speak(self.vc, ctx, answer, self)
            await self.vc.disconnect()
        
        @self.command(name="stop", pass_context= True)
        async def stop_recording(ctx):
            self.vc.stop_recording() # Stop the recording, finished_callback will shortly after be called
            await ctx.channel.send("Stopped!")
            self.audio_thread.join()
            print("Listening terminated successfully")
            
        @self.command(name="listen", pass_context=True)
        async def listen(ctx: commands.Context):
            """starting live transcription (ASR)"""
            
            async def final_callback(msg, _):
                print(msg)
            
            self.vc : discord.VoiceClient = await ctx.author.voice.channel.connect() # Connect to the voice channel of the author
            
            self.vc.start_recording(discord.sinks.WaveSink(), final_callback, "Finish Listening") # Start the recording
            await ctx.channel.send("Listening...")
            await asyncio.sleep(0.5) # wait to let decoder work a little
            
            self.audio_thread = threading.Thread(
                 target=self.pull_audio, # start pulling audio data
                 args=(self.vc, ctx.author.id)
                )
            self.audio_thread.start()
            
            await asyncio.sleep(6)
            await stop_recording(ctx)
            with add_path(find_binary(os.path.join(self.PROJECT_PATH, "assets/ffmpeg_builds/"), 'ffmpeg')):
                # resample_and_save(self.audio_input, self.audio_input)
                # hw_dec = hw_detection(self.audio_input)
                # print("HW Detection: ", hw_dec) # debug
                result = self.stt.transcribe(audio=self.audio_input, fp16=torch.cuda.is_available())
                self.transcription = "$daibl " + result["text"].strip()
                print(self.transcription)
                ctx.message.content = self.transcription
                await adress_bot(ctx)
            os.remove(self.audio_input)