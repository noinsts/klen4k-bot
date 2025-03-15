import calendar

import discord
from discord.ext import commands


class Calendar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
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
