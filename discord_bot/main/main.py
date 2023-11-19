# daibl_bot.py
import os

from dotenv import load_dotenv

from LLM.ModelCommunicator import ModelCommunicator
from TTS_Bot.DaiblVoice import Voice
from Bot.Daibl import Daibl


def main():
    # credential stored as environment variables (should be locally on every machine)
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")
    GUILD = int(os.getenv("DISCORD_GUILD"))
    HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    PROJECT_PATH = os.getenv("PROJECT_PATH")
    # MODEL = os.getenv("MODEL_PATH") obsolete for now

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


if __name__ == "__main__":
    main()
