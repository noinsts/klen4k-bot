import random

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
            await ctx.send(f"**{member.display_name}** відправлений до **{afk.name}**")


    @commands.command()
    async def roulette(self, ctx):
        guild = self.bot.get_guild(cfg.GUILD_ID)
        voice = ctx.author.voice
        channel = voice.channel
        members = channel.members
        members_names = [member for member in members]

        kick = random.choice(members_names)

        if voice is None:
            await ctx.send("Щоб використовувати цю команду потрібно бути в войсі")
        else:
            await kick.move_to(None)
            await ctx.send(f"З войса **{channel.name}** було кікнуто **{kick.display_name}**, тому що так нада")


async def setup(bot):
    await bot.add_cog(Voice(bot))
