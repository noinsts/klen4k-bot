import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from src.utils import setup_logger


class BotClient(commands.Bot):
    def __init__(self):
        load_dotenv()
        token = os.getenv("TOKEN")

        if not token:
            raise ValueError("TOKEN не знайдено в .env файлі!")

        intents = discord.Intents.default()
        intents.guilds = True
        intents.voice_states = True
        intents.dm_messages = True
        intents.members = True
        intents.messages = True
        intents.message_content = True

        super().__init__(command_prefix=".", intents=intents)

        self.token = token
        self.cogs_list = [
            "cogs.utility.voice", "cogs.fun.chat", "cogs.utility.roles", "cogs.admin.moderation",
            "cogs.api.steam", "cogs.gaming.teams", "cogs.admin.logs", "cogs.utility.cal",
            "cogs.users.birthdays", "cogs.economy.balance", "cogs.economy.taxes", "cogs.api.weather",
            "cogs.utility.coffee", "cogs.users.phones", "cogs.users.color", "cogs.api.wikipedia",
            "cogs.api.reddit", "cogs.gaming.auction", "cogs.users.userinfo", "cogs.economy.exchange"
        ]

        self.log = setup_logger()

    async def setup_hook(self):
        """Функція, яка запускається перед запуском бота."""
        await self.load_cogs()

    async def on_ready(self):
        self.log.info(f'✅ Bot {self.user} is running!')
        await self.tree.sync()
        self.log.info("🔄 Slash commands synced")

    async def on_command(self, ctx):
        self.log.info(f"⌨ {ctx.author} виконав команду: {ctx.command}")

    async def load_cogs(self):
        """Завантаження всіх Cogs."""
        for cog in self.cogs_list:
            try:
                await self.load_extension(cog)
                self.log.info(f"✔ Loaded {cog}")
            except Exception as e:
                self.log.error(f"❌ Failed to load {cog}: {e}")

    def run_bot(self):
        """Метод запуску бота."""
        self.run(self.token)

if __name__ == "__main__":
    bot = BotClient()
    bot.run_bot()
