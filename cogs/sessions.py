import discord
from discord import app_commands
from discord.ext import commands
from dotenv import dotenv_values
from discord.utils import get

config = dotenv_values(".env")

SESSION_CHANNEL_ID = config["SESSION_CHANNEL_ID"]
MGMT_ROLE = config["MGMT_ROLE"]
DIRECTIVE_ROLE = config["DIRECTIVE_ROLE"]

voteCount = 0
votedUsers = []

class Counter(discord.ui.View):
    @discord.ui.button(label="Votes: 0", style=discord.ButtonStyle.blurple)
    async def vote(self, interaction: discord.Interaction, button: discord.ui.Button):
        global voteCount
        global votedUsers
        if interaction.user.id in votedUsers:
            voteCount -= 1
            votedUsers.remove(interaction.user.id)
            await interaction.response.send_message(content="Removed vote!", ephemeral=True)
        else:
            voteCount += 1
            votedUsers.append(interaction.user.id)
            await interaction.response.send_message(content="Added vote!", ephemeral=True)

        button.label = f"Votes: {voteCount}"

        await interaction.message.edit(view=self)

    @discord.ui.button(label="View Voters", style=discord.ButtonStyle.red)
    async def voters(self, interaction: discord.Interaction, button: discord.ui.Button):
        global votedUsers
        mentions = []
        for id in votedUsers:
            mention = f"<@{id}>"
            mentions.append(mention)
        if len(mentions) == 0:
            await interaction.response.send_message(content="No voters at this time.", ephemeral=True)
        else:
            await interaction.response.send_message(content=", ".join(mentions), ephemeral=True)

class sessions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="poll", description="Initiates a session poll.")
    @app_commands.checks.has_any_role(MGMT_ROLE, DIRECTIVE_ROLE)
    async def poll(self, interaction : discord.Interaction, votes : int):
        global voteCount
        global votedUsers
        votedUsers.clear()
        voteCount = 0
        await interaction.response.defer()
        emoji = get(interaction.guild.emojis, name="sfrp")
        channel = self.client.get_channel(int(SESSION_CHANNEL_ID))

        embed = discord.Embed(title=f"{emoji} | Session Poll", color=discord.Color.blue(), description=f"<:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354>\n\n> Hello New York! our Session Poll is now live! Vote up for an amazing session!\n> If you vote you **must** join, failure to join when the session begins will result in moderation!\n\n<:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354>\n\n**`Server Info`**\n\n* Code: nycrpX\n\n* Server Owner: Okbuddyimhere1 \n\n* Server Name: New York City Roleplay I Strict I Exciting\n\n<:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354>\n\n`Reactions Needed:` {votes}\n\n-# Vote Up!!")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")
        message = await channel.send(content="||@everyone||", embed=embed, view=Counter())
        #wait message.add_reaction("✅")

        await interaction.followup.send(content="Sent the session poll message.")

    @app_commands.command(name="ssu", description="Initiates a server start-up.")
    @app_commands.checks.has_any_role(MGMT_ROLE, DIRECTIVE_ROLE)
    async def ssu(self, interaction: discord.Interaction):
        await interaction.response.defer()
        emoji = get(interaction.guild.emojis, name="sfrp")
        channel = self.client.get_channel(int(SESSION_CHANNEL_ID))

        embed = discord.Embed(title=f"{emoji} | Server Start-Up", color=discord.Color.blue(), description="<:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354>\n\n> Our in game server has now started up, join to help us reach a full server! **If you reacted You Must Join!** If you can't join please ping the session hoster and let them know of your absence.\n\n<:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354>\n\n**`Server Info`**\n\n* Code: nycrpX\n\n* Server Owner: Okbuddyimhere1 \n\n* Server Name: New York City Roleplay I Strict I Exciting\n\n<:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354>\n\n-# Vote Up!!")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")

        await channel.send(content="||@everyone||", embed=embed)
        await interaction.followup.send(content="Sent the server start-up message.")

    @app_commands.command(name="ssd", description="Initiates a server shutdown.")
    @app_commands.checks.has_any_role(MGMT_ROLE, DIRECTIVE_ROLE)
    async def ssd(self, interaction: discord.Interaction):
        await interaction.response.defer()
        emoji = get(interaction.guild.emojis, name="sfrp")
        channel = self.client.get_channel(int(SESSION_CHANNEL_ID))

        embed = discord.Embed(title=f"{emoji} | Server Shutdown", color=discord.Color.blue(), description="<:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354>\n\n> The in-game server has now shutdown. If you join within this time you will be moderated. We had an amazing session! Join back another time to re-create the same awesome roleplays.\n\n<:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354>\n\n-# Thanks for joining!")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")

        await channel.send(embed=embed)
        await interaction.followup.send(content="Sent the server shutdown message.")

    @app_commands.command(name="low", description="Sends the low player count message.")
    @app_commands.checks.has_any_role(MGMT_ROLE, DIRECTIVE_ROLE)
    async def ssd(self, interaction: discord.Interaction):
        await interaction.response.defer()
        emoji = get(interaction.guild.emojis, name="sfrp")
        channel = self.client.get_channel(int(SESSION_CHANNEL_ID))

        embed = discord.Embed(title=f"{emoji} | Low Player Count", color=discord.Color.blue(), description="<:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354>\n> Our in-game server has reach a low player count! \n> Join up to help us get a session revive!\n\n**`Server Info`**\n\n* Code: nycrpX\n\n* Server Owner: Okbuddyimhere1 \n\n* Server Name: New York City Roleplay I Strict I Exciting\n\n<:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354>")

        await channel.send(content="<@&1304754036934967418>", embed=embed)
        await interaction.followup.send(content="Sent the low player count message.")

    @app_commands.command(name="full", description="Sends the full server message.")
    @app_commands.checks.has_any_role(MGMT_ROLE, DIRECTIVE_ROLE)
    async def ssd(self, interaction: discord.Interaction):
        await interaction.response.defer()
        emoji = get(interaction.guild.emojis, name="sfrp")
        channel = self.client.get_channel(int(SESSION_CHANNEL_ID))

        embed = discord.Embed(title=f"{emoji} | Full Server", color=discord.Color.blue(), description="<:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354>\n> **Our sessions has been/is full!**\n> **Join up, there's amazing roleplays happening!**\n\n**`Server Info`**\n\n* Code: nycrpX\n\n* Server Owner: Okbuddyimhere1 \n\n* Server Name: New York City Roleplay I Strict I Exciting\n<:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354><:Whiteline:1305260872364724354>")

        await channel.send(embed=embed)
        await interaction.followup.send(content="Sent the full server message.")


async def setup(client):
    await client.add_cog(sessions(client))