import os
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv

try:
    from utilities import baseUtils, database
except ImportError as e:
    raise RuntimeError(f'\n > Failed to load libraries! {e}\n')

def main():
    load_dotenv()
    
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        raise ValueError("BOT_TOKEN is missing in .env file.")

    initial_admin_id = os.getenv('INITIAL_ADMIN_ID')

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

    @client.event
    async def on_ready():
        print(f"Zalogowano jako {client.user}")
        if db.get_users_count() == 0 and initial_admin_id:
            try:
                admin_id_int = int(initial_admin_id)
                db.add_user(admin_id_int)
                user = await client.fetch_user(admin_id_int)
                if user:
                    await user.send("Hej! Zostałeś ustawiony jako główny administrator bota MikroLemon. Twoje konto zostało dodane do bazy danych. Możesz teraz używać komend bota, a także dodawać innych użytkowników!")
                    print(f"Wysłano powitalną wiadomość do administratora: {user.name}")
            except Exception as e:
                print(f"Błąd podczas inicjalizacji pierwszego admina: {e}")

    client.run(bot_token)

if __name__ == "__main__":
    main()