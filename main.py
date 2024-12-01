import discord
import os
from discord.ext import commands
from discord import app_commands
import asyncio
from dotenv import dotenv_values
import json

config = dotenv_values(".env")

TOKEN = config["TOKEN"]
Bot = commands.Bot(command_prefix="?", intents=discord.Intents.all(), help_command=None)

@Bot.event
async def on_ready():
    await Bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="SFRP"))
    print("Bot is connected to discord!")

@Bot.event
async def on_member_join(member):
    with open("cogs/json/warns.json", "r", encoding="UTF-8") as f:
        data = json.load(f)

    data[str(member.id)] = {}
    
    with open("cogs/json/warns.json", "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=4)

@Bot.event
async def on_member_remove(member):
    with open("cogs/json/warns.json", "r", encoding="UTF-8") as f:
        data = json.load(f)

    del data[str(member.id)]

    with open("cogs/json/warns.json", "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=4)

async def load():
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            await Bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with Bot:
        await load()
        await Bot.start(TOKEN)

async def on_tree_error(interaction : discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        return await interaction.response.send_message(f"Command is currently on cooldown! Try again in **{error.retry_after:.2f}** seconds!")
    elif isinstance(error, app_commands.MissingPermissions):
        return await interaction.response.send_message(f"You're missing permissions to use this command.")
    elif isinstance(error, app_commands.MissingRole):
        return await interaction.response.send_message("You're missing the required role to use this command.")
    elif isinstance(error, app_commands.MissingAnyRole):
        return await interaction.response.send_message ("You're missing the required role to use this command.")
    else:
        raise error

Bot.tree.on_error = on_tree_error
asyncio.run(main())