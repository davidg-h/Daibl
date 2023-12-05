import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import sys
import librosa
import numpy as np
import io
import speech_recognition as sr
import whisper
import torch
import traceback

import onnxruntime as rt

sess_opt = rt.SessionOptions()
sess_opt.execution_mode  = rt.ExecutionMode.ORT_PARALLEL
sess_opt.intra_op_num_threads = 8
sess_opt.add_session_config_entry('session.intra_op_thread_affinities', '3,4;5,6;7,8;9,10;11,12;13,14;15,16')
sess_opt.inter_op_num_threads = 1

import asyncio
load_dotenv()
PROJECT_PATH = os.getenv("PROJECT_PATH")
sys.path.append(PROJECT_PATH)
sys.path.append(r"/nfs/scratch/students/nguyenda81452/project/dev/daibl/discord_bot/test/Test_Audio/daibl_audio/STT")

from STT.Hotword.detectionclone import hw_detection
from STT.LiveTranscripe import LiveTranscription
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
        self.stt = LiveTranscription(PROJECT_PATH=PROJECT_PATH)
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
        
    def resample_and_save(self, input_path, output_path, target_sr=16000):
        # Laden der Audiodatei
        audio, sr_orig = librosa.load(input_path, sr=None, mono=True)  # Mono und Original-Abtastrate

        # Resampling auf die Ziel-Abtastrate, falls notwendig
        if sr_orig != target_sr:
            audio = librosa.resample(y=audio, orig_sr=sr_orig, target_sr=target_sr)

        # Konvertieren in 16-Bit-Werte (normales WAV-Format)
        audio_int16 = np.int16(audio / np.max(np.abs(audio)) * 32767)

        # Speichern der resampelten Audiodatei
        with wave.open(output_path, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16 Bit
            wav_file.setframerate(target_sr)
            wav_file.writeframes(audio_int16.tobytes())

    # audio processing
    def pull_audio(self, voice_client : discord.VoiceClient, id):
        while voice_client.recording:
            time.sleep(0.5)
            output_dir = "/nfs/scratch/students/nguyenda81452/project/dev/daibl/discord_bot/test/Test_Audio/daibl_audio/output.wav"
            sink_data = voice_client.sink.audio_data.items()
            try:
                for user_id, data in sink_data:
                    if id == user_id:
                        self.audio_data = data.file
                        self.audio_data.seek(0)
                        with wave.open(output_dir, "wb") as f:
                            f.setnchannels(voice_client.decoder.CHANNELS) # 2
                            f.setsampwidth(voice_client.decoder.SAMPLE_SIZE // voice_client.decoder.CHANNELS) # 2
                            f.setframerate(voice_client.decoder.SAMPLING_RATE) # 48000
                            f.writeframes(self.audio_data.read())
                        with add_path(os.path.join(
                            PROJECT_PATH, "assets/ffmpeg-6.0-full_build/bin")):
                            # hw detection
                            self.resample_and_save(output_dir, output_dir)
                            hw_dec = hw_detection(output_dir)
                            print("HW Detection: ", hw_dec)
                            if hw_dec:
                                result = self.stt.audio_model.transcribe(
                                                output_dir, fp16=torch.cuda.is_available()
                                            )
                                print(result["text"].strip())
                print("Still processing... ", voice_client.recording)
            except Exception as e:
                traceback.print_exc()
                print(e)
                continue
    
    async def finished_callback(self, sink, ctx, author_id):
        print("Fertig")
    
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
                
bot = Daibl('$')
bot.run(TOKEN) # run the bot with the token

