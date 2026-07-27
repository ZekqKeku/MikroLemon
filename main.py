import os
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv

try:
    from utilities import baseUtils
    # Optional imports depending on if user provides them later
    # from utilities import uploader, download, botDatabase
except ImportError as e:
    raise RuntimeError(f'\n > Failed to load libraries! {e}\n')

def main():
    load_dotenv()
    
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        raise ValueError("BOT_TOKEN is missing in .env file.")

    # You can add database and other integrations here when needed
    # data_dir = '/data' if os.path.exists('/.dockerenv') else './data'

    intents = nextcord.Intents.default()
    intents.message_content = True
    intents.voice_states = True
    intents.messages = True
    intents.members = True
    intents.guilds = True

    client = commands.Bot(intents=intents)

    payload = {
        'client': client,
        # 'database': database,
    }

    baseUtils.Loader(payload)

    client.run(bot_token)

if __name__ == "__main__":
    main()