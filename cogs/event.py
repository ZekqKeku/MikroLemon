import os
import nextcord
from nextcord.ext import commands

class EventCog(commands.Cog):
    def __init__(self, client, database):
        self.client = client
        self.db = database
        self.initial_admin_id = os.getenv('INITIAL_ADMIN_ID')

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Zalogowano jako {self.client.user}")
        
        if self.db.get_users_count() == 0 and self.initial_admin_id:
            try:
                admin_id_int = int(self.initial_admin_id)
                self.db.add_user(admin_id_int)
                user = await self.client.fetch_user(admin_id_int)
                if user:
                    await user.send("Hej! Zostałeś ustawiony jako główny administrator bota MikroLemon. Twoje konto zostało dodane do bazy danych. Możesz teraz używać komend bota, a także dodawać innych użytkowników!")
                    print(f"Wysłano powitalną wiadomość do administratora: {user.name}")
            except Exception as e:
                print(f"Błąd podczas inicjalizacji pierwszego admina: {e}")
