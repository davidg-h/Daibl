# daibl_bot.py
import os
import discord

from dotenv import load_dotenv

from GPT.ModelCommunicator import ModelCommunicator
from TTS.DaiblVoice import Voice 

# credential stored in environment variables (should be locally on every machine) 
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
MODEL = os.getenv('MODEL_PATH')

# Client setup
## Client is an object that represents a connection to Discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

modelCommunicatior = ModelCommunicator(MODEL)
voice = Voice()
# as soon as bot connects to the server event is started
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    # bot_test channel is referenced
    channel = client.get_channel(1086951624381059112)

    # console output
    print(
        f'\n{client.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})\n'
        f'{client.user} will post messages to channel:{channel.name}\n'
    )
    
    await channel.send("hi im daibl. At your service", tts=True)

@client.event
async def on_message(message):
    #checks message in every channel
    if message.author == client.user:
        return
    #all infos of message (channel, author, ...)
    print(message)
    
    if message.content.startswith("#daibl"):
        answer = communicateWithModel(message.content.replace("#daibl ", ""))
        
        await message.channel.send(answer)
        await voice.tts(message.author.voice.channel , answer)
        #tts = gtts.gTTS(answer)
        #tts.save("discord_bot\\TTS\\answer.mp3")
        #playsound("discord_bot\\TTS\\answer.mp3")



def communicateWithModel(message):
    promptResult = modelCommunicatior.returnPromptText(message)
    return promptResult

# starting the client (-> last line of file)
client.run(TOKEN)
