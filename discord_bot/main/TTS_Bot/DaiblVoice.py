import asyncio
import discord
import os
import wave
import torch

from TTS.api import TTS


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
                "assets/models/tts-models/david-tts-v2/vits_david-tts-v2-voice-October-26-2023_05+35PM-f3f04d3/best_model_557276.pth",
            ),
            config_path=os.path.join(
                self.PROJECT_PATH,
                "assets/models/tts-models/david-tts-v2/vits_david-tts-v2-voice-October-26-2023_05+35PM-f3f04d3/config.json",
            ),
        ).to(device)

    # Run TTS
    async def TTS(self, voiceChannel, text):
        cwd = os.path.dirname(os.path.abspath(__file__))
        # Text to speech to a file
        self.tts.tts_to_file(
            text=text,
            file_path=cwd + "/output.wav",
        )

        # temporary implementation
        vc = await voiceChannel.connect()

        vc.play(
            discord.FFmpegPCMAudio(
                executable=os.path.join(
                    self.PROJECT_PATH,
                    "assets/ffmpeg-6.0-full_build/bin/ffmpeg.exe",  # (.exe is Windows)
                ),
                # executable= os.path.join(self.PROJECT_PATH, "assets/ffmpeg"), # Linux binary executeable for ffmpeg
                source=cwd + "/output.wav",
            ),
            after=lambda e: print("done"),
        )

        # temporary implementation until bug is fixed
        counter = 0
        with wave.open(cwd + "/output.wav") as mywav:
            duration_seconds = (
                mywav.getnframes() / mywav.getframerate()
            )  # get the audio duration in seconds

        while not counter >= duration_seconds:
            await asyncio.sleep(1)
            counter += 1
        await vc.disconnect()
