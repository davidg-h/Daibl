from typing import Optional

import discord
from discord.ext import commands
from discord.ext.audiorec import NativeVoiceClient
from scrap.question_embedding import get_5_most_similar_documents(message)

class Daibl(commands.Bot):
    '''Bot is only responsible for Discord events/commands'''
    
    def __init__(self, command_prefix, self_bot, guild_id, modelCommunicatior, voice):
        commands.Bot.__init__(self, command_prefix=command_prefix, intents=discord.Intents.default(), self_bot=self_bot)
        self.guild_id = guild_id
        self.modelCommunicatior = modelCommunicatior
        self.voice = voice
        self.add_bot_commands()
    
    async def on_ready(self):
        # bot_test channel is referenced
        channel = self.get_channel(1086951624381059112)

        # get the guild
        guild = self.get_guild(self.guild_id)
        # console output
        print(
            f'\n[INFO]: Daibl now online:'
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
            
        await self.process_commands(message)
    
    # should join the channel and stay as long as there is a user in it
    # pass the Voice client (https://discordpy.readthedocs.io/en/stable/api.html#discord.VoiceChannel.connect)
    # to voice so that it can play the .wav file
    def add_bot_commands(self):
        
        @self.command(name="status", pass_context=True)
        async def status(ctx):
            print(ctx)
            await ctx.channel.send("Hello" + " " + ctx.author.name)
            
        @self.command(name="daibl", pass_context=True)
        async def adress_bot(ctx):
            best_documents = await get_5_most_similar_documents(ctx.message.content) #annahme es ist array
            query="/n".join(best_documents)+"/n"+"in regard of the documents above,anwser the following question: /n"+ctx.message.content.replace("$daibl ", "")
            answer = self.modelCommunicatior.returnPromptText(query)

            await ctx.channel.send(answer)
            await self.voice.TTS(ctx.author.voice.channel , answer)
            
        