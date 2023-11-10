from typing import Union

import discord
from discord.ext import commands

from LLM.ModelCommunicator import ModelCommunicator
from TTS_Bot.DaiblVoice import Voice
from STT.Hotword import detection
from STT.LiveTranscripe import LiveTranscription


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
        self.guild_id = guild_id
        self.modelCommunicator = modelCommunicator
        self.voice = voice
        self.stt = LiveTranscription(PROJECT_PATH=PROJECT_PATH)

        self.vc = None
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

    # should join the channel and stay as long as there is a user in it
    # pass the Voice client (https://discordpy.readthedocs.io/en/stable/api.html#discord.VoiceChannel.connect)
    # to voice so that it can play the .wav file
    def add_bot_commands(self):
        """any commands the bot listens to when the prefix is used"""

        @self.command(name="status", pass_context=True)
        async def status(ctx: commands.Context):
            """greeting author"""
            print(ctx)
            await ctx.channel.send("Hello" + " " + ctx.author.name)

        @self.command(name="hotword", pass_context=True)
        async def hotword(ctx: commands.Context):
            
                await ctx.channel.send("Hotword accepted")

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

        @self.command(name="daibl", pass_context=True)
        async def adress_bot(ctx: commands.Context):
            """communicate with LLM module"""
            answer = self.modelCommunicator.returnPromptText(  # TODO give feedback that the question is processing for example play elevator music
                ctx.message.content.replace("$daibl ", "")
            )

            await ctx.channel.send(answer)
            await self.voice.TTS(ctx.author.voice.channel, answer)

        @self.command(name="listen", pass_context=True)
        async def listen(ctx: commands.Context):
            """starting live transcription (ASR)"""
            transcription: list[str] = await self.stt.transcripe(
                self.stt.audio_model, self.get_channel(1086951624381059112)
            )  # can be later replaced with ctx (context) channel
            # get the transcription and give it to the LLM
            for i in range(len(transcription)):
                full_line = "$daibl " + transcription[i]
            ctx.message.content = full_line
            await adress_bot(ctx)
