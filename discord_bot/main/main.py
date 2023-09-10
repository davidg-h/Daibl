# daibl_bot.py
import os
import discord

from dotenv import load_dotenv

from LLM.ModelCommunicator import ModelCommunicator
from TTS_Bot.DaiblVoice import Voice
from Bot.Daibl import Daibl
from STT.LiveTranscripe import LiveTranscription

# credential stored in environment variables (should be locally on every machine)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = int(os.getenv("DISCORD_GUILD"))
# MODEL = os.getenv("MODEL_PATH") obsolete for now
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Bot setup
## Bot is an object that represents a connection to Discord

modelCommunicatior = ModelCommunicator(HUGGINGFACEHUB_API_TOKEN)
voice = Voice()
stt = LiveTranscription()
bot = Daibl(
    command_prefix="$",
    self_bot=False,
    guild_id=GUILD,
    modelCommunicatior=modelCommunicatior,
    voice=voice,
    stt=stt
)

# starting the bot
bot.run(TOKEN)
