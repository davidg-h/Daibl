import discord
import os
import asyncio

from gtts import gTTS
from mutagen.mp3 import MP3

class Voice:
    
    async def TTS(self, voiceChannel, text):
        cwd = os.path.dirname(os.path.abspath(__file__))
        speech = gTTS(text = text, slow=False)
        speech.save(cwd + "\\answer.mp3")
        
        voiceChannel.play(discord.FFmpegPCMAudio(executable= cwd + "\\ffmpeg-6.0-full_build\\bin\\ffmpeg.exe" , source= cwd + "\\answer.mp3"), after = lambda e: print("done"))
        
    
    
    