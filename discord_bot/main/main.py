# daibl_bot.py
import os
import atexit
import sys
os.environ['TRANSFORMERS_CACHE'] = '/nfs/scratch/students/nguyenda81452/CACHE_DIR/huggingface/hub'
os.environ['HF_HOME'] = '/nfs/scratch/students/nguyenda81452/CACHE_DIR/huggingface'

from dotenv import load_dotenv, find_dotenv
from huggingface_hub import logout

from LLM.ModelCommunicator import ModelCommunicator
from TTS_Bot.DaiblVoice import Voice
from Bot.Daibl import Daibl

def main():
    # credential stored as environment variables (should be locally on every machine)
    load_dotenv(find_dotenv())
    TOKEN = os.getenv("DISCORD_TOKEN")
    GUILD = int(os.getenv("DISCORD_GUILD"))
    HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    PROJECT_PATH = os.getenv("PROJECT_PATH")

    # Bot setup
    # Bot is an object that represents a connection to Discord
    modelCommunicator = ModelCommunicator(HUGGINGFACEHUB_API_TOKEN)
    voice = Voice(PROJECT_PATH)
    bot = Daibl(
        command_prefix="$",
        self_bot=False,
        guild_id=GUILD,
        modelCommunicator=modelCommunicator,
        voice=voice,
        PROJECT_PATH=PROJECT_PATH,
    )

    # starting the bot
    bot.run(TOKEN)

def cleanup():
    print ('Exiting')
    logout()
    sys.exit(0)

if __name__ == "__main__":
    atexit.register(cleanup)
    main()