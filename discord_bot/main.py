# daibl_bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Client is an object that represents a connection to Discord
intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)

channel = client.get_channel(1086951624381059112)
print(channel)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    
    await channel.send("Im here")

client.run(TOKEN)