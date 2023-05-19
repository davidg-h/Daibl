# daibl_bot.py
import os
import discord

from dotenv import load_dotenv

from GPT.ModelCommunicator import ModelCommunicator
from TTS.DaiblVoice import Voice 
from Bot.Daibl import Daibl

# credential stored in environment variables (should be locally on every machine) 
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = int(os.getenv('DISCORD_GUILD'))
MODEL = os.getenv('MODEL_PATH')

# Client setup
## Client is an object that represents a connection to Discord
intents = discord.Intents.default()
intents.message_content = True

modelCommunicatior = ModelCommunicator(MODEL)
voice = Voice()
bot = Daibl(
    intents = intents, 
    guild_id= GUILD, 
    modelCommunicatior = modelCommunicatior, 
    voice = voice ,
    command_prefix="#daibl"
    )

# starting the bot
bot.run(TOKEN)
