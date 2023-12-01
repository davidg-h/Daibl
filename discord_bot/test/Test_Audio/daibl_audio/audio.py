import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import sys

import speech_recognition as sr
import whisper
import torch

import asyncio
load_dotenv()
PROJECT_PATH = os.getenv("PROJECT_PATH")
sys.path.append(PROJECT_PATH)
sys.path.append("/nfs/scratch/students/nguyenda81452/project/dev/daibl/discord_bot/test/Test_Audio/daibl_audio/STT")

from STT.Hotword.detectionclone import detect_hotword
from util.Environment import add_path

# voice channel listening
import wave
import time
import threading


TOKEN = os.getenv("DISCORD_TOKEN")

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
    ):
        commands.Bot.__init__(
            self,
            command_prefix=command_prefix,
            intents=discord.Intents.all(),
        )
        self.vc = None
        self.audio_thread = None
        #self.whisper = whisper.load_model('small').to('cuda:0') # testing if audio gets transcriped
        self.add_bot_commands()

    async def on_ready(self):
        """start up routine"""
        # bot_test channel is referenced
        channel = self.get_channel(1086951624381059112)

        # get the guild
        # console output
        print(
            f"\n[INFO]: Daibl now online:"
            f"\n{self.user} is connected to the following guild:\n"
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
        user_data = None
        while voice_client.recording:
            time.sleep(1)
            try:
                for user_id, data in voice_client.sink.audio_data.items():
                    if id == user_id:
                        user_data = data.file
                        ### hotword ###
                    if detect_hotword(user_data):
                        print("Hotword erkannt!")
                user_data.seek(0) # move pointer to begin of file
                with wave.open('./output.wav', 'wb') as wave_file:
                    wave_file.setnchannels(voice_client.decoder.CHANNELS)
                    wave_file.setsampwidth(voice_client.decoder.SAMPLE_SIZE // voice_client.decoder.CHANNELS)
                    wave_file.setframerate(voice_client.decoder.SAMPLING_RATE)
                    
                    # Write the audio data to the wave file
                    wave_file.writeframes(user_data.read())
                print("Still processing... ", voice_client.recording)
            except Exception as e:
                print(e)
                continue
        print(user_data)
    
    async def finished_callback(self, sink, ctx, author_id):
        # # Hotword detection
        # if hw_detection(wav):
        #     await ctx.channel.send("HW ggeeeeht!")
        #     # transcribe
        # with add_path(os.path.join(PROJECT_PATH, "assets/ffmpeg-6.0-full_build/bin")):
        #     result = self.whisper.transcribe(
        #         "./daibl_audio/output.wav", fp16=torch.cuda.is_available()
        #     )
        # text = result["text"].strip()
        # print(text)
        print("Fertig")
            
        # antwort vom bot
        # play antwort in voice channel 
    
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
                self.vc.disconnect()
                pass

        @self.command(name="dc", pass_context=True)
        async def disconnect(ctx: commands.Context):
            """disconnect voice channel"""
            try:
                await self.vc.disconnect()
            except Exception as e:
                print(e)
                pass
             
        @self.command(name="stop", pass_context= True)
        async def stop_recording(ctx):
            self.vc.stop_recording() # Stop the recording, finished_callback will shortly after be called
            await ctx.channel.send("Stopped!")
            await self.vc.disconnect()
            self.audio_thread.join()
            print("Listening terminated successfully")
            
        @self.command(name="listen", pass_context= True)
        async def start_record(ctx):
            
            self.vc : discord.VoiceClient = await ctx.author.voice.channel.connect() # Connect to the voice channel of the author
            
            self.vc.start_recording(discord.sinks.WaveSink(), self.finished_callback, ctx, ctx.author.id) # Start the recording
            
            await ctx.channel.send("Listening...")
            await asyncio.sleep(1) # wait to let decoder work a little
            self.audio_thread = threading.Thread(
                 target=self.pull_audio, # start pulling audio data
                args=(self.vc, ctx.author.id)
                )
            self.audio_thread.start()
        
        @self.command(name="hw", pass_context= True)
        async def hw_dect(ctx):
            try:
                if hw_detection():
                    await ctx.channel.send("HW Klappt")
            except Exception as e:
                print(e)
            
                
bot = Daibl('$')
bot.run(TOKEN) # run the bot with the token

