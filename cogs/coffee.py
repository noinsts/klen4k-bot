import random

import discord
from discord.ext import commands

from database import Database


class Coffee(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.db = Database()

    ##


class CoffeeView(discord.ui.View):
    def __init__(self):
        super().__init__()

    ##

async def setup(bot):
    await bot.add_cog(Coffee(bot))
