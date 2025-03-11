import discord
from discord.ext import commands

from database import Database

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
    async def balance(self, ctx):
        member = ctx.author
        pass

        """SHOW YOUR BALANCE"""


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            pass


    @commands.command()
    async def change_tax(self, action: str, amount: int):
        pass

        """CHANGE TAX AMOUNT"""


    """SHOW/HIDE TAX LOGS LOCATED IN logs.py"""


async def setup(bot):
    await bot.add_cog(Balance(bot))
