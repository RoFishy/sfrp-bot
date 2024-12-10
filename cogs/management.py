import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
from dotenv import dotenv_values
import uuid
import json
import time
import datetime
from dispie import EmbedCreator

config = dotenv_values(".env")

DIRECTIVE_ROLE = config["DIRECTIVE_ROLE"]
IA_ROLE = config["IA_ROLE"]
MGMT_ROLE = config["MGMT_ROLE"]

INFRACT_CHANNEL_ID = config["INFRACT_CHANNEL_ID"]
PROMOTE_CHANNEL_ID = config["PROMOTE_CHANNEL_ID"]
LOGGING_CHANNEL_ID = config["LOGGING_CHANNEL_ID"]

def add_user_to_infractions_json(user : discord.Member):
    with open("cogs/json/staff.json", "r", encoding="UTF-8") as f:
        data = json.load(f)
    
    data[str(user.id)] = {}

    with open("cogs/json/staff.json", "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=4)

def add_infractions_json(user, moderator, punishment, reason):
    if punishment != "retire":
        with open("cogs/json/staff.json", "r", encoding="UTF-8") as f:
            data = json.load(f)
        if str(user.id) in data:
            global prev
            if str(punishment) in data[str(user.id)]:
                prev = len(data[str(user.id)][str(punishment)])
            else:
                data[str(user.id)][punishment] = {}
                prev=0

            uniqueId = uuid.uuid4()
            data[str(user.id)][punishment][prev] = {
                "Moderator" : str(moderator.id),
                "Reason" : str(reason),
                "Date" : str(datetime.date.today()),
                "ID" : str(uniqueId)
            }

            with open("cogs/json/staff.json", "w", encoding="UTF-8") as f:
                data = json.dump(data, f, indent=4)
        else:
            add_user_to_infractions_json(user)
            time.sleep(1)
            add_infractions_json(user, moderator, punishment, reason)

class management(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} loaded successfully!")

    @app_commands.command(name="infract", description="Infracts the given staff member.")
    @app_commands.describe(punishment="Punishment to give the user.")
    @app_commands.choices(punishment=[
        app_commands.Choice(name="Strike", value="strike"),
        app_commands.Choice(name="Warning", value="warn"),
        app_commands.Choice(name="Termination", value="term"),
        app_commands.Choice(name="Retirement", value="retire")
    ])
    @app_commands.checks.has_any_role(DIRECTIVE_ROLE, IA_ROLE, MGMT_ROLE)
    async def infract(self, interaction: discord.Interaction, user: discord.Member, reason: str, punishment: app_commands.Choice[str]):
        emoji = get(interaction.guild.emojis, name="sfrp")

        infract_embed = discord.Embed(title=f"{emoji} | Infraction", color=discord.Color.orange()) if punishment.value != "retire" else discord.Embed(title=f"{emoji} | Retirement", color=discord.Color.orange())
        infract_embed.add_field(name="", value="", inline=False)
        infract_embed.add_field(name="", value=f"> **User:** {user.mention}\n> **Reason:** {reason}\n> **Punishment:** {punishment.name}\n> **Moderator:** {interaction.user.mention}", inline=False) if punishment.value != "retire" else infract_embed.add_field(name="", value=f"> **User:** {user.mention}\n> **Reason/Message:** {reason}\n> **Moderator:** {interaction.user.mention}\n\nWe thank them for their service. o7 :saluting_face:", inline=False)
        infract_embed.add_field(name="", value="\n *If this was false open a ticket in <#1117544480405467157>*") if punishment.value != "retire" else None
        infract_embed.set_footer(text="Powered by SFRP", icon_url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")
        infract_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")

        embed = discord.Embed(title="⚠️ Staff Infraction", color=discord.Color.red()) if punishment.value != "retire" else discord.Embed(title="Retirement", color=discord.Color.orange())
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")
        embed.add_field(name="", value=f"You have received an infraction in SFRP for violating the rules.\n\n> **Moderator:** {interaction.user.mention}\n> **Reason:** {reason}\n> **Punishment:** {punishment.name}\n\n-# *If this was false open a ticket in <#1117544480405467157>.*") if punishment.value != "retire" else embed.add_field(name="", value=f"You have been retired from the staff team. Thank you for your service. o7 :saluting_face:\n\n> **Moderator:** {interaction.user.mention}\n> **Reason/Message:** {reason}\n\n-# *If this was false open a ticket in <#1117544480405467157>.*")
        embed.set_footer(text="Powered by SFRP", icon_url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")
        
        channel = self.client.get_channel(int(INFRACT_CHANNEL_ID))
        await channel.send(content=user.mention, embed=infract_embed)
        await interaction.response.send_message("Successfully infracted the user.")
        await user.send(embed=embed)
        add_infractions_json(user, interaction.user, punishment.value, reason)

    @app_commands.command(name="infractions-view", description="View a user's past staff infractions.")
    async def view(self, interaction : discord.Interaction, member : discord.Member = None):
        with open("cogs/json/staff.json", "r", encoding="UTF-8") as f:
            data = json.load(f)
        member = member or interaction.user
        userInfo = data[str(member.id)]
        embed = discord.Embed(title="Staff Infractions", color=discord.Color.red())
        for type, infractions in userInfo.items():
            global infract_type_full
            if type=="strike":
                embed.add_field(name="__Strikes__", value="")
                infract_type_full = "Strike"
            elif type=="term":
                embed.add_field(name="__Terminations__", value="")
                infract_type_full = "Termination"
            elif type=="warn":
                embed.add_field(name="__Warns__", value="")
                infract_type_full = "Warn"

            for current in infractions:
                infraction = infractions[current]
                embed.add_field(name=f"{infract_type_full} #{current}", value=f"> **Moderator:** <@{int(infraction['Moderator'])}>\n> **Reason:** {infraction['Reason']}\n> **Date:** {infraction['Date']}\n> **ID:** {infraction['ID']}", inline=False)
        embed.set_footer(text="Powered by SFRP", icon_url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")
        await interaction.response.send_message(embed=embed) 

    @app_commands.command(name="infraction-delete", description="Deletes a staff infraction using the given ID.")       
    @app_commands.checks.has_any_role(DIRECTIVE_ROLE, IA_ROLE, MGMT_ROLE)
    async def delete(self, interaction : discord.Interaction, user : discord.Member, id : str):
        await interaction.response.defer()
        with open("cogs/json/staff.json", "r", encoding="UTF-8") as f:
            data = json.load(f)
        userInfo = data[str(user.id)]
        found = False
        for type, infractions in userInfo.items():
            for current in infractions:
                infraction = infractions[current]
                if infraction['ID'] == id:
                    del infractions[current]
                    await interaction.followup.send(f"Successfully deleted infraction with ID: {id}")
                    found = True
                    break
        if found == False:
            await interaction.followup.send(f"Infraction with id: {id} not found for user.")

        with open("cogs/json/staff.json", "w", encoding="UTF-8") as f:
            json.dump(data, f, indent=4)

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

    @app_commands.command(name="say", description="Have the bot say the inputted text.")
    @app_commands.checks.has_any_role(DIRECTIVE_ROLE)
    async def say(self, interaction : discord.Interaction, message : str, channel : discord.TextChannel = None):
        channel = channel or interaction.channel
        await channel.send(message)
        await interaction.response.send_message(content="Sent message.", ephemeral=True)

    @app_commands.command(name="create-embed", description="Opens the embed builder")
    @app_commands.checks.has_any_role(DIRECTIVE_ROLE)
    async def create_embed(self, interaction : discord.Interaction):
        view = EmbedCreator(bot=self.client)
        await interaction.response.send_message(embed=view.get_default_embed, view=view)

async def setup(client):
    await client.add_cog(management(client))