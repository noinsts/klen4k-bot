import calendar

import discord
from discord.ext import commands

from src.cogs.base import BaseCog


class Calendar(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)


    @commands.hybrid_command(
        name = 'calendar',
        description = 'Відображає календар'
    )
    async def calendar(self, ctx, mode: str, year: int, month: int = None):
        if mode == 'month':
            if month is None or month not in range(1, 13):
                await ctx.send('Вкажи правильно місяць (число від 1 до 12)')
                return
            else:
                cal = f'```{calendar.month(year, month)}```'
        elif mode == 'year':
            await ctx.send('Помилка, **year** поки що не доступний')
            return
        else:
            await ctx.send('Правильно введи значення: .calendar month/year, year (int), month (int)')
            return


        await ctx.send(cal)


async def setup(bot):
    await bot.add_cog(Calendar(bot))
