import nextcord
from nextcord.ext import commands
import os
import routeros_api
import time

class ConnectedDevicesCog(commands.Cog):
    def __init__(self, client, database):
        self.client = client
        self.db = database
        self.host = os.getenv('MIKROTIK_HOST')
        self.user = os.getenv('MIKROTIK_USER')
        self.password = os.getenv('MIKROTIK_PASS')
        self._networks_cache = []
        self._networks_last_fetch = 0

    async def cog_application_command_check(self, interaction: nextcord.Interaction):
        if not self.db.is_authorized(interaction.user.id):
            await interaction.response.send_message("Nie jesteś autoryzowany do korzystania z tego bota.", ephemeral=True)
            return False
        return True

    def get_pool(self):
        return routeros_api.RouterOsApiPool(
            self.host, 
            username=self.user, 
            password=self.password,
            plaintext_login=True
        )

    def _fetch_networks(self):
        try:
            pool = self.get_pool()
            api = pool.get_api()
            addresses = api.get_resource('/ip/address').get()
            networks = []
            for addr in addresses:
                if 'network' in addr:
                    networks.append(addr['network'])
                if 'address' in addr:
                    networks.append(addr['address'].split('/')[0])
            pool.disconnect()
            return list(set(networks))
        except Exception as e:
            from utilities.logger import log
            log.error(f"Error fetching networks: {e}")
            return []

    @nextcord.slash_command(name="connected", description="Wyświetla wszystkie połączone urządzenia w danej sieci")
    async def connected(self, interaction: nextcord.Interaction, network: str = nextcord.SlashOption(description="Wybierz lub wpisz sieć (np. 192.168.75.1)", autocomplete=True)):
        await interaction.response.defer(ephemeral=False)
        
        try:
            pool = self.get_pool()
            api = pool.get_api()
            leases = api.get_resource('/ip/dhcp-server/lease').get()
            pool.disconnect()
            
            connected_devices = []
            search_prefix = network.rsplit('.', 1)[0] if '.' in network else network
            
            for lease in leases:
                if 'address' in lease and lease.get('status') == 'bound':
                    if network in lease['address'] or lease['address'].startswith(search_prefix):
                        connected_devices.append(lease)
            
            if not connected_devices:
                await interaction.followup.send(f"Nie znaleziono połączonych urządzeń dla: **{network}**.")
                return
                
            embed = nextcord.Embed(title=f"Połączone urządzenia - {network}", color=0x3498db)
            
            for dev in connected_devices[:25]:
                ip = dev.get('address', 'Brak IP')
                mac = dev.get('mac-address', 'Brak MAC')
                hostname = dev.get('host-name', 'Nieznane urządzenie')
                embed.add_field(name=hostname, value=f"**IP:** {ip}\n**MAC:** {mac}", inline=False)
                
            if len(connected_devices) > 25:
                embed.set_footer(text=f"Pokazano 25 z {len(connected_devices)} urządzeń.")
            else:
                embed.set_footer(text=f"Znaleziono urządzeń: {len(connected_devices)}")
                
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            await interaction.followup.send(f"Wystąpił błąd podczas łączenia z RouterOS:\n```{e}```")

    @connected.on_autocomplete("network")
    async def connected_autocomplete(self, interaction: nextcord.Interaction, current: str):
        now = time.time()
        if now - self._networks_last_fetch > 60:
            fetched = self._fetch_networks()
            if fetched:
                self._networks_cache = fetched
                self._networks_last_fetch = now
                
        choices = [net for net in self._networks_cache if current.lower() in net.lower()][:25]
        
        if not choices and not self._networks_cache:
            choices = ["Wpisz adres sieci..."]
            
        await interaction.response.send_autocomplete(choices)
