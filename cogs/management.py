import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
from dotenv import dotenv_values
import datetime

config = dotenv_values(".env")

DIRECTIVE_ROLE = config["DIRECTIVE_ROLE"]
IA_ROLE = config["IA_ROLE"]
MGMT_ROLE = config["MGMT_ROLE"]

INFRACT_CHANNEL_ID = config["INFRACT_CHANNEL_ID"]
PROMOTE_CHANNEL_ID = config["PROMOTE_CHANNEL_ID"]
LOGGING_CHANNEL_ID = config["LOGGING_CHANNEL_ID"]

class management(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print(f"{__name__} loaded successfully!")

    @app_commands.command(name="infract", description="Infracts the given staff member.")
    @app_commands.checks.has_any_role(DIRECTIVE_ROLE, IA_ROLE, MGMT_ROLE)
    async def infract(self, interaction: discord.Interaction, user: discord.Member, reason: str, outcome: str):
        emoji = get(interaction.guild.emojis, name="sfrp")
        line = "**-**"

        infract_embed = discord.Embed(title=f"{emoji} | Infraction", color=discord.Color.blue())
        infract_embed.add_field(name="", value=f"{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}", inline=False)
        infract_embed.add_field(name="Moderator: ", value=interaction.user.mention, inline=False)
        infract_embed.add_field(name="User: ", value=user.mention, inline=False)
        infract_embed.add_field(name="Reason: ", value=reason, inline=False)
        infract_embed.add_field(name="Outcome: ", value=outcome, inline=False)
        infract_embed.add_field(name="", value="\n *If this was false open a ticket in <#1304575261358162032>*")
        infract_embed.set_footer(text="Powered by SFRP", icon_url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")

        channel = self.client.get_channel(int(INFRACT_CHANNEL_ID))
        await channel.send(content=user.mention, embed=infract_embed)
        await interaction.response.send_message("Successfully infracted the user.")

    @app_commands.command(name="promote", description="Promotes the given staff member.")
    @app_commands.checks.has_any_role(DIRECTIVE_ROLE, IA_ROLE, MGMT_ROLE)
    async def promote(self, interaction: discord.Interaction, user: discord.Member, reason: str, new_rank: str, old_rank: str):
        emoji = get(interaction.guild.emojis, name="sfrp")
        line = "**-**"

        infract_embed = discord.Embed(title=f"{emoji} | Staff Promotion", color=discord.Color.orange())
        infract_embed.add_field(name="", value=f"Congrats on getting promoted!", inline=False)
        infract_embed.add_field(name="", value=f"> **User:** {user.mention}\n> **Old Rank:** {old_rank}\n> **New Rank:** {new_rank}\n> **Reason:** {reason}\n> **Moderator:** {interaction.user.mention}", inline=False)
        infract_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")
        infract_embed.set_footer(text=f"Powered by SFRP", icon_url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")


        channel = self.client.get_channel(int(PROMOTE_CHANNEL_ID))
        await channel.send(content=user.mention, embed=infract_embed)
        await interaction.response.send_message("Successfully promoted the user.")

async def setup(client):
    await client.add_cog(management(client))