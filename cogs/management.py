import os
import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
from dotenv import dotenv_values

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
        emoji = get(interaction.guild.emojis, name="nycrp")
        line = get(interaction.guild.emojis, name="BlueLine")

        infract_embed = discord.Embed(title=f"{emoji} | Infraction", color=discord.Color.blue())
        infract_embed.add_field(name="", value=f"{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}", inline=False)
        infract_embed.add_field(name="Moderator: ", value=interaction.user.mention, inline=False)
        infract_embed.add_field(name="User: ", value=user.mention, inline=False)
        infract_embed.add_field(name="Reason: ", value=reason, inline=False)
        infract_embed.add_field(name="Outcome: ", value=outcome, inline=False)
        infract_embed.add_field(name="", value="\n *If this was false open a ticket in <#1304575261358162032>*")
        infract_embed.set_footer(text="Powered by NYCRP", icon_url="https://cdn.discordapp.com/attachments/1305269939162320946/1308544269128044614/NYCRP_SERVER_LOGO.png?ex=673e5451&is=673d02d1&hm=b2b82704abc59ce686f730da31cee671b61d68d9386f8412fd38d26f5e9be2f9&")

        channel = self.client.get_channel(int(INFRACT_CHANNEL_ID))
        await channel.send(content=user.mention, embed=infract_embed)
        await interaction.response.send_message("Successfully infracted the user.")

    @app_commands.command(name="promote", description="Promotes the given staff member.")
    @app_commands.checks.has_any_role(DIRECTIVE_ROLE, IA_ROLE, MGMT_ROLE)
    async def promote(self, interaction: discord.Interaction, user: discord.Member, reason: str, new_rank: str, old_rank: str):
        emoji = get(interaction.guild.emojis, name="nycrp")
        line = get(interaction.guild.emojis, name="BlueLine")

        infract_embed = discord.Embed(title=f"{emoji} | Promotion", color=discord.Color.blue())
        infract_embed.add_field(name="", value=f"{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}", inline=False)
        infract_embed.add_field(name="Moderator: ", value=interaction.user.mention, inline=False)
        infract_embed.add_field(name="User: ", value=user.mention, inline=False)
        infract_embed.add_field(name="Reason: ", value=reason, inline=False)
        infract_embed.add_field(name="Old Rank: ", value=old_rank, inline=False)
        infract_embed.add_field(name="New Rank: ", value=new_rank, inline=False)
        infract_embed.set_footer(text="Powered by NYCRP", icon_url="https://cdn.discordapp.com/attachments/1305269939162320946/1308544269128044614/NYCRP_SERVER_LOGO.png?ex=673e5451&is=673d02d1&hm=b2b82704abc59ce686f730da31cee671b61d68d9386f8412fd38d26f5e9be2f9&")

        channel = self.client.get_channel(int(PROMOTE_CHANNEL_ID))
        await channel.send(content=user.mention, embed=infract_embed)
        await interaction.response.send_message("Successfully promoted the user.")

async def setup(client):
    await client.add_cog(management(client))