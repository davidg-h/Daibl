import asyncio
import threading
from uu import Error
import discord
from discord.ext import commands
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import wave
import torch

from TTS.api import TTS
from util.Antiblocking import run_blocking, run_async_in_thread
from util.Environment import find_binary


class Voice:
    """TTS module"""

    def __init__(self, PROJECT_PATH: str):
        self.PROJECT_PATH = PROJECT_PATH
        # Get device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        # List available 🐸TTS models
        # print(f"coqui-ai TTS models:\n{TTS().list_models()}\n")

        # Init TTS
        self.tts = TTS(
            model_path=os.path.join(
                self.PROJECT_PATH,
                "assets/models/tts-models/vincent-tts-v1/vits_vincent-tts-v1-voice-January-12-2024_05+48PM-0000000/best_model.pth", # !!Change!! to your voice model
            ),
            config_path=os.path.join(
                self.PROJECT_PATH,
                "assets/models/tts-models/vincent-tts-v1/vits_vincent-tts-v1-voice-January-12-2024_05+48PM-0000000/config.json", # !!Change!! to your voice model
            ),
            gpu=True
        ).to(device)

    # Run TTS
    async def speak(self, vc : discord.VoiceClient, ctx: commands.Context, text, client):
        cwd = os.path.dirname(os.path.abspath(__file__))
        
        try:
            vc : discord.VoiceClient = await ctx.author.voice.channel.connect()
        except discord.ClientException:
            vc : discord.VoiceClient = vc
        
        t = threading.Thread(target=run_async_in_thread, args=(self.play_waiting_music, vc))
        t.start()
        
        # Text to speech to a file
        await run_blocking(self.tts.tts_to_file, client, text=text, file_path=cwd + "/output.wav")
        
        t.output_done = True
        vc.stop()
        ffmpeg_executable_dir = find_binary(os.path.join(self.PROJECT_PATH, "assets/ffmpeg_builds/"), 'ffmpeg')
        vc.play(
            discord.FFmpegPCMAudio(executable=os.path.join(ffmpeg_executable_dir, 'ffmpeg') , source=cwd + "/output.wav",
            ),
            after=lambda e: print("done talking"),
        )
        
        counter = 0
        with wave.open(cwd + "/output.wav") as mywav:
            duration_seconds = (
                mywav.getnframes() / mywav.getframerate()
            )  # get the audio duration in seconds

        while not counter >= duration_seconds:
            await asyncio.sleep(1)
            counter += 1
            
        os.remove(cwd + "/output.wav")
        return vc

    async def play_waiting_music(self, vc : discord.VoiceClient):
        t = threading.currentThread()
        # elevator_music = "/nfs/scratch/students/nguyenda81452/project/dev/daibl/discord_bot/main/TTS_Bot/elevator.mp3"
        elevator_music=os.path.join(
                self.PROJECT_PATH,
                "discord_bot/main/TTS_Bot/elevator.mp3",
            )
        ffmpeg_executable_dir = find_binary(os.path.join(self.PROJECT_PATH, "assets/ffmpeg_builds/"), 'ffmpeg')
        vc.play(
            discord.FFmpegPCMAudio(executable=os.path.join(ffmpeg_executable_dir, 'ffmpeg'), source=elevator_music,
            ),
            after=lambda e: print("done playing elevator musdic"),
        )
        while not getattr(t, "output_done", False):
            await asyncio.sleep(1)
        return