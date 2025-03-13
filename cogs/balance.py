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


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            tax = self.db.amount_tax("join_voice")  # змінено на "join_voice"

            if tax is None:
                print("Помилка: податок для 'join_voice' не знайдено в БД!")
                return

            self.db.update_balance(member.id, tax)

            if self.db.is_log_allowed("tax_logs"):
                log_channel = member.guild.get_channel(cfg.LOG_CHANNEL_ID)

                if log_channel:
                    embed = discord.Embed(
                        title='Новий податок!',
                        description=f'**{member.display_name}** зайшов у войс, з нього знято {tax} грошей',
                        color=discord.Color.red()
                    )
                    await log_channel.send(embed=embed)


    @commands.command()
    @commands.has_permissions(administrator = True)
    async def change_tax(self, ctx, action: str, amount: int):
        self.db.set_taxes(action, amount)
        await ctx.send('Податок змінено')


    """SHOW/HIDE TAX LOGS LOCATED IN logs.py"""


async def setup(bot):
    await bot.add_cog(Balance(bot))
