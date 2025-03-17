import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN не знайдено в .env файлі!")

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True
intents.dm_messages = True
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

cogs = [
    "cogs.voice", "cogs.chat", "cogs.roles", "cogs.moderation",
    "cogs.steam", "cogs.teams", "cogs.logs", "cogs.cal", 
    "cogs.birthdays", "cogs.balance", "cogs.taxes", "cogs.weather", 
    "cogs.coffee"
]

@bot.event
async def on_ready():
    print(f'Bot {bot.user} is run!')
    await bot.wait_until_ready()
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f"Loaded {cog}")
        except Exception as e:
            print(f"Failed to load {cog}: {e}")

if __name__ == "__main__":
    bot.run(TOKEN)
