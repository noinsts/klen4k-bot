from discord.ext import commands

from src.database import Database
from src.utils.json import JSONLoader
from src.utils.logger import setup_logger


class BaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
        self.cfg = JSONLoader()
        self.log = setup_logger()
