import os
import sqlite3

import discord
from discord.ext import commands

from dotenv import load_dotenv

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True
intents.dm_messages = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

cogs = ["cogs.voice", "cogs.chat", "cogs.roles", "cogs.moderation",
        "cogs.steam", "cogs.teams", "cogs.logs", "cogs.cal", "cogs.birthdays"]


@bot.event
async def on_ready():
    print(f'Bot {bot.user} is run!')
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f"Loaded {cog}")
        except Exception as e:
            print(f"Failed to load {cog}: {e}")

if __name__ == "__main__":
    load_dotenv()
    bot.run(os.getenv("TOKEN"))