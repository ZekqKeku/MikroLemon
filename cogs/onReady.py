import os
import nextcord
from nextcord.ext import commands
from utilities.logger import log

class OnreadyCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(f"Podstawowe dzne bota:")
        log.info(f"Nazwa: {self.client.user}")
        log.info(f"ID: {self.client.user.id}")
        log.info(f"Ping bota: {round(self.client.latency * 1000)}ms")
        
        invite_link = f"https://discordapp.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=8&scope=bot"
        log.info(f"Link do zaproszenia: {invite_link}")
        
        data_dir = '/data' if os.path.exists('/.dockerenv') else './data'
        os.makedirs(data_dir, exist_ok=True)
        with open(os.path.join(data_dir, 'invite.txt'), 'w', encoding='utf-8') as f:
            f.write(invite_link)
