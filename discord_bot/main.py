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


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    channel = client.get_channel(1086951624381059112)

    print(
        f'\n{client.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})\n'
        f'{client.user} will post messages to channel:{channel.name}\n'
    )

    await channel.send("hi im daibl. At your service")


# is the last line in file
client.run(TOKEN)
