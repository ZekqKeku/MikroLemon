import nextcord
from nextcord.ext import commands

class AdminCog(commands.Cog):
    def __init__(self, client, database):
        self.client = client
        self.db = database

    async def cog_application_command_check(self, interaction: nextcord.Interaction):
        if not self.db.is_authorized(interaction.user.id):
            await interaction.response.send_message("Nie jesteś autoryzowany do korzystania z tego bota.", ephemeral=True)
            return False
        return True

    @nextcord.slash_command(name="user", description="Zarządzanie autoryzowanymi użytkownikami")
    async def user_group(self, interaction: nextcord.Interaction):
        pass

    @user_group.subcommand(name="add", description="Dodaj nowego autoryzowanego użytkownika")
    async def add_user(self, interaction: nextcord.Interaction, user: nextcord.User = nextcord.SlashOption(description="Wybierz użytkownika do dodania")):
        self.db.add_user(user.id)
        await interaction.response.send_message(f"Użytkownik {user.mention} został dodany do bazy autoryzowanych osób.", ephemeral=True)

    @user_group.subcommand(name="remove", description="Usuń autoryzowanego użytkownika")
    async def remove_user(self, interaction: nextcord.Interaction, user: nextcord.User = nextcord.SlashOption(description="Wybierz użytkownika do usunięcia")):
        if self.db.get_users_count() <= 1:
            await interaction.response.send_message("Nie możesz usunąć użytkownika, ponieważ w bazie musi pozostać przynajmniej jedna autoryzowana osoba (inaczej nikt nie będzie miał dostępu).", ephemeral=True)
            return
        
        success = self.db.remove_user(user.id)
        if success:
            await interaction.response.send_message(f"Użytkownik {user.mention} został usunięty z bazy autoryzowanych osób.", ephemeral=True)
        else:
            await interaction.response.send_message("Nie udało się usunąć użytkownika (np. zabezpieczenie przed usunięciem ostatniego).", ephemeral=True)

    @user_group.subcommand(name="list", description="Wypisz wszystkich autoryzowanych użytkowników")
    async def list_users(self, interaction: nextcord.Interaction):
        users = self.db.get_all_users()
        user_mentions = [f"<@{uid}>" for uid in users]
        await interaction.response.send_message(f"Autoryzowani użytkownicy:\n" + "\n".join(user_mentions), ephemeral=True)
