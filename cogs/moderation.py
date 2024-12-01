import discord
from discord import app_commands
from discord.ext import commands
from dotenv import dotenv_values
import datetime
import json
import uuid

config = dotenv_values(".env")

MODERATION_ROLE = config["DISCORD_MODERATION_ROLE"]
DIRECTIVE_ROLE = config["DIRECTIVE_ROLE"]
IA_ROLE = config["IA_ROLE"]
MGMT_ROLE = config["MGMT_ROLE"]
LOGGING_CHANNEL_ID = config["LOGGING_CHANNEL_ID"]

class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    role = app_commands.Group(
        name="role",
        description="Adjusts the roles of users."
    )

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print(f"{__name__} loaded successfully!")

    @role.command(name="add", description="Adds a role to a user.")
    @app_commands.checks.has_any_role(DIRECTIVE_ROLE, MGMT_ROLE, IA_ROLE)
    async def role_add(self, interaction : discord.Interaction, member : discord.Member, role : discord.Role):
        if interaction.user.top_role.position > role.position:
            try:
                await member.add_roles(role)
            except Exception as e:
                await interaction.response.send_message(e)

            conf_embed = discord.Embed(title = "Member Roled", color=discord.Color.blue())
            conf_embed.add_field(name="Moderator: ",value=interaction.user.mention, inline=False)
            conf_embed.add_field(name="Roled: ", value=member.mention, inline=False)
            conf_embed.add_field(name="New Role: ", value=role.mention, inline=False)
            conf_embed.set_footer(text="Powered by SFRP", icon_url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")

            channel = self.client.get_channel(int(LOGGING_CHANNEL_ID))
            await channel.send(embed=conf_embed)
            await interaction.response.send_message(f"Successfuly roled user {member.mention}")
        else:
            await interaction.response.send_message(f"Cannot add role to user {member.mention}.")

    @role.command(name="remove", description="Removes a role from a user.")
    @app_commands.checks.has_any_role(DIRECTIVE_ROLE, MGMT_ROLE, IA_ROLE)
    async def role_remove(self, interaction : discord.Interaction, member : discord.Member, role : discord.Role):
        if interaction.user.top_role.position > role.position:
            try:
                await member.remove_roles(role)
            except Exception as e:
                await interaction.response.send_message(e)

            conf_embed = discord.Embed(title = "Role Removed", color=discord.Color.blue())
            conf_embed.add_field(name="Moderator: ",value=interaction.user.mention, inline=False)
            conf_embed.add_field(name="Roled: ", value=member.mention, inline=False)
            conf_embed.add_field(name="Removed Role: ", value=role.mention, inline=False)
            conf_embed.set_footer(text="Powered by SFRP", icon_url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")

            channel = self.client.get_channel(int(LOGGING_CHANNEL_ID))
            await channel.send(embed=conf_embed)
            await interaction.response.send_message(f"Successfuly removed role from user {member.mention}")
        else:
            await interaction.response.send_message(f"Cannot remove role from user {member.mention}.")

    @app_commands.command(name="purge", description="Purges above messages.")
    @app_commands.checks.has_any_role(MODERATION_ROLE, DIRECTIVE_ROLE)
    async def purge(self, interaction : discord.Interaction, count : int):
        await interaction.response.send_message(f"Purged {count} message(s).", ephemeral=True)

        await interaction.channel.purge(limit=count)
        conf_embed = discord.Embed(title = "Message Purged", color=discord.Color.blue(), url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")
        conf_embed.add_field(name="Moderator: ",value=interaction.user.mention, inline=False)
        conf_embed.add_field(name="Messages: ", value=count, inline=False)
        conf_embed.add_field(name="Channel: ", value=interaction.channel)
        
        channel = self.client.get_channel(int(LOGGING_CHANNEL_ID))
        
        await channel.send(embed=conf_embed)

    @app_commands.command(name="kick", description="Kicks the given user")
    @app_commands.checks.has_any_role(MODERATION_ROLE, DIRECTIVE_ROLE)
    async def kick(self, interaction : discord.Interaction, member: discord.Member, *, reason : str):
        if interaction.user.top_role.position > member.top_role.position:
            try:
                await interaction.guild.kick(user=member, reason=reason)
            except Exception as e:
                await interaction.response.send_message(e)

            conf_embed = discord.Embed(title = "Member Kicked", color=discord.Color.blue())
            conf_embed.add_field(name="Moderator: ",value=interaction.user.mention, inline=False)
            conf_embed.add_field(name="Kicked: ", value=member.mention, inline=False)
            conf_embed.add_field(name="Reason: ", value=reason, inline=False)
            conf_embed.set_footer(text="Powered by SFRP", icon_url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")

            channel = self.client.get_channel(int(LOGGING_CHANNEL_ID))
            await channel.send(embed=conf_embed)

            await interaction.response.send_message(f"Kicked user: {member.mention}.")
        else:
            await interaction.response.send_message(f"Cannot kick user {member.mention}.")

    @app_commands.command(name="ban", description="Bans the given user")
    @app_commands.checks.has_any_role(MODERATION_ROLE, DIRECTIVE_ROLE)
    async def ban(self, interaction : discord.Interaction, member: discord.Member, reason : str):
        if interaction.user.top_role.position > member.top_role.position:
            try:
                await interaction.guild.ban(user=member, reason=reason)
            except Exception as e:
                await interaction.response.send_message(e)

            conf_embed = discord.Embed(title = "Member Banned", color=discord.Color.blue())
            conf_embed.add_field(name="Moderator: ",value=interaction.user.mention, inline=False)
            conf_embed.add_field(name="Banned: ", value=member.mention, inline=False)
            conf_embed.add_field(name="Reason: ", value=reason, inline=False)
            conf_embed.set_footer(text="Powered by SFRP", icon_url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")

            channel = self.client.get_channel(int(LOGGING_CHANNEL_ID))
            await channel.send(embed=conf_embed)

            await interaction.response.send_message(f"Banned user: {member.mention}.")
        else:
            await interaction.response.send_message(f"Cannot ban user {member.mention}.")

    @app_commands.command(name="unban", description="Unbans the given user by their ID.")
    @app_commands.checks.has_any_role(MODERATION_ROLE, DIRECTIVE_ROLE)
    async def unban(self, interaction : discord.Interaction, member : discord.Member, id : int, reason : str):
        await interaction.response.defer()
        user = await self.client.fetch(id)
        try:
            await interaction.guild.unban(user=user, reason=reason)
        except Exception as e:
            await interaction.response.send_message(e)
        
        await interaction.followup.send(f"Unbanned user.")
        conf_embed = discord.Embed(title = "Member Unbanned", color=discord.Color.blue())
        conf_embed.add_field(name="Moderator: ",value=interaction.user.mention, inline=False)
        conf_embed.add_field(name="Unbanned: ", value=member.mention, inline=False)
        conf_embed.add_field(name="Reason: ", value=reason, inline=False)
        conf_embed.set_footer(text="Powered by SFRP", icon_url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")

        channel = self.client.get_channel(int(LOGGING_CHANNEL_ID))
        await channel.send(embed=conf_embed)

    @app_commands.command(name='mute', description='Mutes a user for a specific time')
    @app_commands.checks.has_any_role(MODERATION_ROLE, DIRECTIVE_ROLE)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0, reason: str = None):
        duration = datetime.timedelta(seconds=seconds, minutes=minutes, hours= hours, days=days)
        if duration:
            try:
                await member.timeout(duration, reason=reason)
            except Exception as e:
                await interaction.response.send_message(e)
        else:
            try:
                await member.timeout(reason=reason)
            except Exception as e:
                await interaction.response.send_message(e)

        conf_embed = discord.Embed(title = "Member Muted", color=discord.Color.blue())
        conf_embed.add_field(name="Moderator: ",value=interaction.user.mention, inline=False)
        conf_embed.add_field(name="Muted: ", value=member.mention, inline=False)
        conf_embed.add_field(name="Duration: ", value=duration, inline=False)
        conf_embed.add_field(name="Reason: ", value=reason, inline=False)
        conf_embed.set_footer(text="Powered by SFRP", icon_url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")

        channel = self.client.get_channel(int(LOGGING_CHANNEL_ID))
        await channel.send(embed=conf_embed)

        await interaction.response.send_message(f'{member.mention} was muted for {duration}')

    @app_commands.command(name='unmute', description='Unmutes a user')
    @app_commands.checks.has_any_role(MODERATION_ROLE, DIRECTIVE_ROLE)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        try:
            await member.timeout(None,reason=reason)
        except Exception as e:
            await interaction.response.send_message(e)

        conf_embed = discord.Embed(title = "Member Unmuted", color=discord.Color.blue())
        conf_embed.add_field(name="Moderator: ",value=interaction.user.mention, inline=False)
        conf_embed.add_field(name="Unmuted: ", value=member.mention, inline=False)
        conf_embed.add_field(name="Reason: ", value=reason, inline=False)
        conf_embed.set_footer(text="Powered by SFRP", icon_url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")

        channel = self.client.get_channel(int(LOGGING_CHANNEL_ID))
        await channel.send(embed=conf_embed)

        await interaction.response.send_message(f'{member.mention} was unmuted.')

    @app_commands.command(name="setup-mutes", description="Developer command.")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup(self, interaction : discord.Interaction):
        with open("cogs/json/warns.json", "r", encoding="UTF-8") as f:
            data = json.load(f)

        for member in interaction.guild.members:
            data[str(member.id)] = {}
        
        with open("cogs/json/warns.json", "w", encoding="UTF-8") as f:
            json.dump(data, f, indent=4)
        await interaction.response.send_message("Setup warns.")

    @app_commands.command(name="warn", description="Warns a user")
    @app_commands.checks.has_any_role(MODERATION_ROLE, DIRECTIVE_ROLE)
    async def warn(self, interaction : discord.Interaction, member : discord.Member, reason : str):
        with open("cogs/json/warns.json", "r", encoding="UTF-8") as f:
            data = json.load(f)

        prevInfractions = len(data[str(member.id)])
        if prevInfractions != 0:
            prevInfractions += 1

        uniqueId = uuid.uuid4()
        data[str(member.id)][prevInfractions] = {
            "Moderator" : str(interaction.user.id),
            "Reason" : reason,
            "Date" : str(datetime.date.today()),
            "ID" : str(uniqueId)
        }
        with open("cogs/json/warns.json", "w", encoding="UTF-8") as f:
            json.dump(data, f, indent=4)

        await interaction.response.send_message(f"Successfully warned user {member.mention} for {reason}")

    @app_commands.command(name="view-warns", description="Gets a list of warns of a user.")
    async def view_warns(self, interaction : discord.Interaction, member : discord.Member = None):
        await interaction.response.defer()
        member = member or interaction.user
        with open("cogs/json/warns.json", "r", encoding="UTF-8") as f:
            data = json.load(f)
        userInfo = data[str(member.id)]
        embed = discord.Embed(title="Previous Infractions", color=discord.Color.red())
        for current, infraction in userInfo.items():
            if current == 0:
                current = 1
            embed.add_field(name=f"Infraction #{current}", value=f"> **Moderator:** <@{int(infraction['Moderator'])}>\n> **Reason:** {infraction['Reason']}\n> **Date:** {infraction['Date']}\n> **ID:** {infraction['ID']}", inline=False)
        embed.set_footer(text="Powered by SFRP", icon_url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="delwarn", description="Delete's a user's warn using the given ID.")
    @app_commands.checks.has_any_role(MODERATION_ROLE, DIRECTIVE_ROLE)
    async def del_warn(self, interaction : discord.Interaction, member : discord.Member, id : str):
        await interaction.response.defer()
        with open("cogs/json/warns.json", "r", encoding="UTF-8") as f:
            data = json.load(f)
        userInfo = data[str(member.id)]
        found = False
        for number, infraction in userInfo.items():
            if infraction['ID'] == id:
                del userInfo[number]
                await interaction.followup.send(f"Successfully deleted warn with ID: {id}")
                found = True
                break
        if found == False:
            await interaction.followup.send(f"Warn with id: {ID} not found for user.")

        with open("cogs/json/warns.json", "w", encoding="UTF-8") as f:
            json.dump(data, f, indent=4)
   

async def setup(client):
    await client.add_cog(moderation(client))