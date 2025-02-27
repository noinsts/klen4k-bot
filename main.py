import os

import discord
from discord.ext import commands

import config as cfg

from dotenv import load_dotenv

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True
intents.dm_messages = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

cogs = ["cogs.voice"]


@bot.event
async def on_ready():
    print(f'Bot {bot.user} is run!')
    for cog in cogs:
        await bot.load_extension(cog)


if __name__ == "__main__":
    load_dotenv()
    bot.run(os.getenv("TOKEN"))
