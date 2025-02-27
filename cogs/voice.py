import discord
from discord.ext import commands

import config as cfg


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def afk(self, ctx, member: discord.Member):
        guild = self.bot.get_guild(cfg.GUILD_ID)
        afk = guild.get_channel(cfg.AFK_ID)
        voice = member.voice

        if voice is None:
            await ctx.send("Помилка, цієї людини немає в войсі")
        else:
            await member.move_to(afk)
            await ctx.send(f"**{member.name}** відправлений до **{afk.name}**")



async def setup(bot):
    await bot.add_cog(Voice(bot))
