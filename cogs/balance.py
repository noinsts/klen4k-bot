import discord
from discord.ext import commands

from database import Database

import config as cfg

class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def change_balance(self, ctx, amount: int, member: discord.Member = None):
        if not member:
            member = ctx.author

        if amount == 0:
            await ctx.send(f'Баланс користувача **{member.display_name}** не змінено.')
            return

        self.db.update_balance(member.id, amount)  # запит на зміну балансу

        if amount > 0:
            await ctx.send(f'Баланс користувача **{member.display_name}** збільшено на **{amount}** 💸')
        else:
            await ctx.send(f'Баланс користувача **{member.display_name}** зменшено на **{-amount}** 💸')

    @commands.command()
    async def balance(self, ctx, member: discord.Member = None):
        if not member:
            balance = self.db.get_balance(ctx.author.id)
            await ctx.send(f'Ваш баланс **{balance}** гривень 💸')
        else:
            balance = self.db.get_balance(member.id)
            await ctx.send(f'Баланс користувача **{member.display_name}** **{balance}** гривень 💸')


async def setup(bot):
    await bot.add_cog(Balance(bot))
