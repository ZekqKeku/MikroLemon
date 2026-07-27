try:
    import os
    import nextcord
    from nextcord.ext import commands
    from dotenv import load_dotenv
    from utilities import baseUtils, database
except ImportError as e:
    raise RuntimeError(f'\n > Failed to load libraries! {e}\n')

def main():
    load_dotenv()
    
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        raise ValueError("BOT_TOKEN is missing in .env file.")

    data_dir = '/data' if os.path.exists('/.dockerenv') else './data'
    db = database.Database(data_dir, 'mikrolemon.db')

    intents = nextcord.Intents.default()
    intents.message_content = True
    intents.voice_states = True
    intents.messages = True
    intents.members = True
    intents.guilds = True

    client = commands.Bot(intents=intents)

    payload = {
        'client': client,
        'database': db,
    }

    baseUtils.Loader(payload)

    client.run(bot_token)

if __name__ == "__main__":
    main()