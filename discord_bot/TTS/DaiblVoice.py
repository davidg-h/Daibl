import discord
import os
import asyncio

from gtts import gTTS
from mutagen.mp3 import MP3

class Voice:
    
    def audio_len(self, path):
        audio = MP3(path)
        return audio.info.length
    
    async def tts(self, voiceChannel, text):
        speech = gTTS(text = text, slow=False)
        speech.save("discord_bot\\TTS\\answer.mp3")
        
        vc = await voiceChannel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="discord_bot\\TTS\\ffmpeg-6.0-full_build\\bin\\ffmpeg.exe" , source="answer.mp3"), after = lambda e: print("done"))
        
        counter = 0
        cwd = os.getcwd()
        duration = self.audio_len(cwd + "\\answer.mp3")
        while not counter >= duration:
            await asyncio.sleep(1)
            counter += 1
        await vc.disconnect()
    
    
    