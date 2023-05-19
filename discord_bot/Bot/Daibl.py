from typing import Optional

import discord
from discord.ext import commands

class Daibl(commands.Bot):
    '''Bot is only responsible for Discord events/commands'''
    
    def __init__(
        self,
        *args,
        guild_id: Optional[int] = None,
        modelCommunicatior,
        voice,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.guild_id = guild_id
        self.modelCommunicatior = modelCommunicatior
        self.voice = voice
    
    async def on_ready(self):
        # bot_test channel is referenced
        channel = self.get_channel(1086951624381059112)

        # get the guild
        guild = self.get_guild(self.guild_id)
        # console output
        print(
            f'\n{self.user} is connected to the following guild:\n'
            f'{guild.name} (id: {guild.id})\n'
            f'{self.user} will post messages to channel:{channel.name}\n'
        )
        
        await channel.send("hi im daibl. At your service", tts=True)
    
    async def on_message(self, message):
        #checks message in every channel
        if message.author == self.user:
            return
        
        #all infos of message (channel, author, ...)
        print(message)
        
        answer = self.modelCommunicatior.returnPromptText(message.content.replace("#daibl ", ""))
        
        await message.channel.send(answer)
        await self.voice.TTS(message.author.voice.channel , answer)
    
    voice_client = None    
    async def on_voice_state_update(self, member, before, after):
        global voice_client
        if before.channel is None and after.channel is not None:
            # Ein Mitglied hat einen Sprachkanal betreten
            channel = after.channel
            # Bot dem Sprachkanal beitreten lassen
            await channel.connect()
        if before.channel is not None and after.channel is None:
           if voice_client and voice_client.channel == before.channel and len(before.channel.members) == 1:
            # Der Bot ist der einzige übrig im Kanal, also trenne die Verbindung
            await voice_client.disconnect()
            voice_client = None  # Setze die VoiceClient-Referenz zurück
        