import discord
from discord import app_commands
from discord.ext import commands
import datetime, time
from dotenv import dotenv_values
import uuid
import time
import json

config = dotenv_values(".env")

DIRECTIVE_ROLE = config["DIRECTIVE_ROLE"]
IA_ROLE = config["IA_ROLE"]
MGMT_ROLE = config["MGMT_ROLE"]

RATING_CHANNEL = config["REVIEW_CHANNEL_ID"]

def add_user_to_fb_json(user : discord.Member):
    with open("cogs/json/feedback.json", "r", encoding="UTF-8") as f:
        data = json.load(f)
    
    data[str(user.id)] = {}

    with open("cogs/json/feedback.json", "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=4)

def add_feedback_json(user, submitter, rating, reason, date):
    with open("cogs/json/feedback.json", "r", encoding="UTF-8") as f:
        data = json.load(f)
    if str(user.id) in data:
        prev = len(data[str(user.id)])

        uniqueId = uuid.uuid4()
        data[str(user.id)][prev] = {
            "Submitter" : str(submitter.id),
            "Rating" : str(rating),
            "Feedback" : str(reason),
            "Date" : str(datetime.date.today()),
            "ID" : str(uniqueId)
        }

        with open("cogs/json/feedback.json", "w", encoding="UTF-8") as f:
            data = json.dump(data, f, indent=4)
    else:
        add_user_to_fb_json(user)
        time.sleep(1)
        add_feedback_json(user, submitter, rating, reason, date)

class maincmds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        global startTime
        startTime = time.time()
        print(f"{__name__} loaded successfully!")

    @app_commands.command(name="ping", description="Shows the bot's current latency.")
    async def ping(self, interaction : discord.Interaction):
        embed = discord.Embed(title="🏓 | Pong!", color=discord.Color.orange())
        embed.add_field(name="Ping:", value=f"{round(self.client.latency) * 1000}ms")

        currentTime = time.time()
        diff = int(round(currentTime-startTime))
        text = str(datetime.timedelta(seconds=diff))
        embed.add_field(name="Uptime:", value=text)
        embed.set_footer(text="Powered by SFRP", icon_url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")

        await interaction.response.send_message(embed=embed)

    feedback = app_commands.Group(
        name="feedback",
        description="Manage staff feedback!"
    )

    @feedback.command(name="submit", description="Rate a staff member!")
    @app_commands.describe(rating="Rating to give the staff member")
    @app_commands.choices(rating=[
        discord.app_commands.Choice(name="⭐", value=1),
        discord.app_commands.Choice(name="⭐⭐", value=2),
        discord.app_commands.Choice(name="⭐⭐⭐", value=3),
        discord.app_commands.Choice(name="⭐⭐⭐⭐", value=4),
        discord.app_commands.Choice(name="⭐⭐⭐⭐⭐", value=5),
    ])
    async def submit(self, interaction : discord.Interaction, staff_member : discord.Member, rating : discord.app_commands.Choice[int], feedback: str):
        await interaction.response.defer()
        channel = self.client.get_channel(int(RATING_CHANNEL))
        embed = discord.Embed(title="Staff Feedback", color=discord.Color.orange())
        embed.add_field(name="Staff Member", value=staff_member.mention, inline=True)
        embed.add_field(name="Rating", value=rating.name, inline=True)
        embed.add_field(name="Feedback",value=feedback,inline=False)
        embed.add_field(name="", value="-# Feedback ID: ####",inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")
        embed.set_footer(text="Powered by SFRP", icon_url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")

        add_feedback_json(staff_member, interaction.user, rating.name, feedback, datetime.date.today)
        await channel.send(content=staff_member.mention, embed=embed)
        await interaction.followup.send("Submitted feedback!")

    @feedback.command(name="view", description="View a staff member's feedback!")
    async def view(self, interaction : discord.Interaction, member : discord.Member = None):
        with open("cogs/json/feedback.json", "r", encoding="UTF-8") as f:
            data = json.load(f)
        member = member or interaction.user
        userInfo = data[str(member.id)]
        embed = discord.Embed(title="Staff Feedback", color=discord.Color.orange())
        for current, feedback in userInfo.items():
            if current == 0:
                current = 1
            embed.add_field(name=f"Feedback #{current}", value=f"> **Submitter:** <@{int(feedback['Submitter'])}>\n> **Rating:** {feedback['Rating']}\n> **Feedback:** {feedback['Feedback']}\n> **Date:** {feedback['Date']}\n> **ID:** {feedback['ID']}", inline=False)
        embed.set_footer(text="Powered by SFRP", icon_url="https://cdn.discordapp.com/attachments/1308174353279488009/1310587102706008135/my-image_44-2.png?ex=674dabda&is=674c5a5a&hm=4729d8fe8bcb8331f010cce47b3c5ae4d61ee72fcd7abc18f619d06eeedb6540&")
        await interaction.response.send_message(embed=embed)

    @feedback.command(name="delete", description="Delete a staff feedback entry using the given ID.")
    @app_commands.checks.has_any_role(DIRECTIVE_ROLE, IA_ROLE, MGMT_ROLE)
    async def delete(self, interaction : discord.Interaction, user : discord.Member, id : str):
        await interaction.response.defer()
        with open("cogs/json/feedback.json", "r", encoding="UTF-8") as f:
            data = json.load(f)
        userInfo = data[str(user.id)]
        found = False
        for number, feedback in userInfo.items():
            if feedback['ID'] == id:
                del userInfo[number]
                await interaction.followup.send(f"Successfully deleted feedback with ID: {id}")
                found = True
                break
        if found == False:
            await interaction.followup.send(f"Feedback with id: {id} not found for user.")

        with open("cogs/json/feedback.json", "w", encoding="UTF-8") as f:
            json.dump(data, f, indent=4)


async def setup(client):
    await client.add_cog(maincmds(client))