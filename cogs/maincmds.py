import discord
from discord import app_commands
from discord.ext import commands
import datetime, time

class maincmds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print(f"{__name__} loaded successfully!")
        self.startTime = time.time()

    @app_commands.command(name="ping", description="Show's the bot's current latency.")
    async def ping(self, interaction : discord.Interaction):
        embed = discord.Embed(title="🏓 | Pong!", color=discord.Color.orange())
        embed.add_field(name="Ping:", value=f"{round(self.client.latency) * 1000}ms")

        currentTime = time.time()
        diff = int(round(currentTime-self.startTime))
        text = str(datetime.timedelta(seconds=diff))
        embed.add_field(name="Uptime:", value=text)
        embed.set_footer(text="Powered by SFRP", icon_url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")

        await interaction.response.send_message(embed=embed)

async def setup(client):
    await client.add_cog(maincmds(client))