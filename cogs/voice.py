import discord
from discord.ext import commands

import config as cfg


class Voice(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    """
    COMMANDS HERE
    """


async def setup(bot):
    await bot.add_cog(Voice(bot))
