import nextcord
from nextcord.ext import commands

class HelloWorldCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="hello", description="Says hello world!")
    async def hello(self, interaction: nextcord.Interaction):
        await interaction.response.send_message("Hello World! MikroLemon is ready.")
