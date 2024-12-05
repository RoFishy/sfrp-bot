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
    @discord.ui.button(label="Votes: 0", style=discord.ButtonStyle.blurple, custom_id="vote")
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

    @discord.ui.button(label="View Voters", style=discord.ButtonStyle.red, custom_id="view-votes") 
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

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} loaded successfully!")

    @app_commands.command(name="sync")
    @app_commands.checks.has_permissions(administrator=True)
    async def sync(self, interaction : discord.Interaction):
        await interaction.response.defer()
        fmt = await self.client.tree.sync()
        await interaction.followup.send(f"Synced {len(fmt)} commands.")

    sessions_group = app_commands.Group(
        name="session",
        description="Session commands."
    )
        
    @sessions_group.command(name="poll", description="Initiates a session poll.")
    @app_commands.checks.has_any_role(MGMT_ROLE, DIRECTIVE_ROLE)
    async def poll(self, interaction : discord.Interaction, votes : int):
        global voteCount
        global votedUsers
        votedUsers.clear()
        voteCount = 0
        emoji = get(interaction.guild.emojis, name="sfrp")
        channel = self.client.get_channel(int(SESSION_CHANNEL_ID))

        embed = discord.Embed(title=f"{emoji} | Session Poll", color=discord.Color.orange(), description=f"A session vote has been initiated! If you vote during this time, you are required to join the in-game server within 15 minutes to avoid moderation!\n\nVotes needed: {votes}\n-# Vote up!")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1131850933551239173/1308024411118374953/SFRP_SSV_embed.png?ex=674d93a9&is=674c4229&hm=d1cff433f6064dcb6fb775ab341df54942e5ad593613b7fec25dccb638600218&")
        view = Counter(timeout=None)
        await channel.send(embed=embed, view=view)

        await interaction.followup.send(content="Sent the session poll message.")

    @sessions_group.command(name="startup", description="Initiates a server start-up.")
    @app_commands.checks.has_any_role(MGMT_ROLE, DIRECTIVE_ROLE)
    async def ssu(self, interaction: discord.Interaction):
        await interaction.response.defer()
        emoji = get(interaction.guild.emojis, name="sfrp")
        channel = self.client.get_channel(int(SESSION_CHANNEL_ID))

        embed = discord.Embed(title=f"{emoji} | Server Start-Up", color=discord.Color.orange(), description="A session has been initiated! If you voted during the voting period, you are required to join the server to avoid moderation!\n\n- Server Owner: `anse1125`\n- Server Name: `San Francisco Roleplay | Custom Liveries | Strict`\n- Server Code: `SFrp`")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1131850933551239173/1308023863011049564/SFRP_SSU_embed.png?ex=674d9326&is=674c41a6&hm=a533bb1c24d6766e5ea7942bf535581b45dab0f5356ec020c561ac7de343cbc1&")

        await channel.send(embed=embed)
        await interaction.followup.send(content="Sent the server start-up message.")

    @sessions_group.command(name="shutdown", description="Initiates a server shutdown.")
    @app_commands.checks.has_any_role(MGMT_ROLE, DIRECTIVE_ROLE)
    async def ssd(self, interaction: discord.Interaction):
        await interaction.response.defer()
        emoji = get(interaction.guild.emojis, name="sfrp")
        channel = self.client.get_channel(int(SESSION_CHANNEL_ID))

        embed = discord.Embed(title=f"{emoji} | Server Shutdown", color=discord.Color.orange(), description="The in-game server has now shutdown! During this period, do not join the in-game server or moderation actions may be taken against you! Another session will occur shortly, thank you!\n\n-# Thanks for joining!")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1131850933551239173/1308024114946113597/SFRP_SSD_EMBED.png?ex=674d9362&is=674c41e2&hm=469f2926a220fc26afa5c101de6bb38591f48bbf70a84805445e64fb9c135102&")

        await channel.send(embed=embed)
        await interaction.followup.send(content="Sent the server shutdown message.")

    @sessions_group.command(name="low", description="Sends the low player count message.")
    @app_commands.checks.has_any_role(MGMT_ROLE, DIRECTIVE_ROLE)
    async def low(self, interaction: discord.Interaction):
        await interaction.response.defer()
        emoji = get(interaction.guild.emojis, name="sfrp")
        channel = self.client.get_channel(int(SESSION_CHANNEL_ID))

        embed = discord.Embed(title=f"{emoji} | Low Player Count", color=discord.Color.orange(), description="Our in-game server has reach a low player count! \nJoin up to help us get a session revive!\n\nCode: `SFrp`\n\nServer Owner: `anse1125` \n\nServer Name: San Francisco Roleplay | Custom Liveries | Strict\n\n")

        await channel.send(embed=embed)
        await interaction.followup.send(content="Sent the low player count message.")

    @sessions_group.command(name="full", description="Sends the full server message.")
    @app_commands.checks.has_any_role(MGMT_ROLE, DIRECTIVE_ROLE)
    async def ssd(self, interaction: discord.Interaction):
        await interaction.response.defer()
        emoji = get(interaction.guild.emojis, name="sfrp")
        channel = self.client.get_channel(int(SESSION_CHANNEL_ID))

        embed = discord.Embed(title=f"{emoji} | Full Server", color=discord.Color.orange(), description="The in-game server is now full! Keep trying to join for some amazing, professional roleplays!")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1131850933551239173/1308023332091990037/SFRP_Server_FUll_embed.png?ex=674d92a8&is=674c4128&hm=c1683adbc29f99924b80711899e9a28a70dfd9889702694b96d7f5779e8d7f78&")
        await channel.send(embed=embed)
        await interaction.followup.send(content="Sent the full server message.")


async def setup(client):
    await client.add_cog(sessions(client))