import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from src.cogs.base import BaseCog


class Balance(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)


    @commands.hybrid_command(
        name = 'change_balance',
        description = 'Змінює баланс вказаного користувача (тільки адміністратор)'
    )
    @commands.has_permissions(administrator=True)
    async def change_balance(self, ctx, amount: int, member: discord.Member = None):
        if not member:
            member = ctx.author

        if amount == 0:
            await ctx.send(f'Баланс користувача **{member.display_name}** не змінено.')
            return

        self.db.balance.update_balance(member.id, amount)  # запит на зміну балансу

        if amount > 0:
            await ctx.send(f'Баланс користувача **{member.display_name}** збільшено на **{amount}** 💸')
        else:
            await ctx.send(f'Баланс користувача **{member.display_name}** зменшено на **{-amount}** 💸')


    @commands.hybrid_command(
        name = 'balance',
        description = 'Відображає ваш баланс'
    )
    async def balance(self, ctx, member: discord.Member = None):
        if not member:
            balance = self.db.balance.get_balance(ctx.author.id)
            await ctx.send(f'Ваш баланс **{balance}** гривень 💸')
        else:
            balance = self.db.balance.get_balance(member.id)
            await ctx.send(f'Баланс користувача **{member.display_name}** **{balance}** гривень 💸')


    @commands.hybrid_command(
        name = 'balance_tier_list',
        description = 'Список мажорів серверу'
    )
    async def balance_tier_list(self, ctx):
        result = self.db.balance.balance_tier_list()
        
        if not result:
            await ctx.send('Інформації не знайдено, спробуйте пізніше')
            return
        
        embed = discord.Embed(title='Тір-ліст за балансом', color=discord.Color.gold())

        medals = ['🥇', '🥈', '🥉']
        for index, (user_id, balance) in enumerate(result, start=1):
            user = ctx.guild.get_member(user_id)
            if user:
                medal = medals[index - 1] if index <= 3 else f'{index}'
                embed.add_field(name=f'{medal} **{user.display_name}**', value = f'{balance}$', inline=False)
        await ctx.send(embed=embed)


    @commands.hybrid_command(
        name = 'balance_privacy',
        description = 'Дозволяє змінити налаштування приватності вашого балансу'
    )
    async def balance_privacy(self, ctx):
        state = 1 if not self.db.balance.get_balance_privacy(ctx.author.id) else 0
        self.db.balance.set_balance_privacy(state, ctx.author.id)
        await ctx.send(f'Статус приватності балансу змінено на **{bool(state)}**')


    """
    DANGER ZONE
    """


    @commands.command()
    # залишаємо без змін
    @commands.has_permissions(administrator = True)
    async def clear_balances(self, ctx, password: str):
        if not password:
            await ctx.send('Введіть пароль')
            return

        load_dotenv()
        correct = os.getenv('PASSWORD')

        if password != correct:
            await ctx.send('Введіть правильний пароль')
            return

        self.db.balance.clear_balances()

        await ctx.send('**BALANCES DATABASE IS CLEAR**')


async def setup(bot):
    await bot.add_cog(Balance(bot))
