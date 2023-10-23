import asyncio
import discord
import os
import wave

from TTS.api import TTS

class Voice: # https://tts.readthedocs.io/en/dev/inference.html for own model
    """ TTS module """
    def __init__(self):
        # List available 🐸TTS models and choose the first one
        self.model_name = TTS.list_models()[0]
        # Init TTS
        self.tts = TTS(self.model_name)

    # Run TTS
    # ❗ Since this model is multi-speaker and multi-lingual, we must set the target speaker and the language
    # Text to speech with a numpy output
    async def TTS(self, voiceChannel, text):
        cwd = os.path.dirname(os.path.abspath(__file__))
        # Text to speech to a file
        self.tts.tts_to_file(
            text=text,
            speaker=self.tts.speakers[0],
            language=self.tts.languages[0],
            file_path=cwd + "/output.wav",
        )
      

        # temporary implementation
        vc = await voiceChannel.connect()
     
        vc.play(
            discord.FFmpegPCMAudio(
                executable="assets/ffmpeg-6.0-full_build/bin/ffmpeg.exe", # (.exe is Windows)
                # executable= cwd + "/app/assets/ffmpeg", # Linux binary executeable for ffmpeg
                source=cwd + "/output.wav",
            ),
            after=lambda e: print("done"),
        )
        
        # temporary implementation until bug is fixed
        counter = 0
        with wave.open(cwd+ "/output.wav") as mywav:
            duration_seconds = mywav.getnframes() / mywav.getframerate() # get the audio duration in seconds
        
        while not counter >= duration_seconds:
            await asyncio.sleep(1)
            counter += 1
        await vc.disconnect()
        
