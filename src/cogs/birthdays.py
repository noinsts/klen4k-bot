import datetime
import discord
from discord.ext import commands
from src.database import Database  # Імпортуємо клас для роботи з БД

class Birthdays(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()  # Створюємо підключення до БД

    @commands.command()
    async def add_birthday(self, ctx, date: str, member: discord.Member = None):
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            await ctx.send("Невірний формат дати, спробуйте YYYY-MM-DD")
            return

        if member is None:
            member = ctx.author

        self.db.add_birthday(member.id, date)
        await ctx.send(f'Дата народження **{date}** для користувача **{member.display_name}** записана')

    @commands.command()
    async def update_birthday(self, ctx, date: str, member: discord.Member = None):
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            await ctx.send('Невірний формат дати, спробуйте YYYY-MM-DD')
            return

        if member is None:
            member = ctx.author

        self.db.update_birthday(member.id, date)
        await ctx.send(f'Дата народження користувача **{member.display_name}** оновлена до **{date}**')

    @commands.command()
    async def remove_birthday(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        self.db.remove_birthday(member.id)
        await ctx.send(f'Дата народження користувача **{member.display_name}** видалена')

    @commands.command()
    async def birthday(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        result = self.db.get_birthday(member.id)
        if result:
            await ctx.send(f'День народження користувача **{member.display_name}**: **{result[0]}**')
        else:
            await ctx.send(f'Дата народження користувача **{member.display_name}** не знайдена')

    @commands.command()
    async def birthday_list(self, ctx):
        results = self.db.get_all_birthdays()

        if not results:
            await ctx.send('Немає збережених днів народження')
            return

        embed = discord.Embed(title='Список днів народження', color=0x00FF00)

        for user_id, birthday_str in results:
            try:
                user = await self.bot.fetch_user(user_id)
                embed.add_field(name=user.display_name, value=birthday_str, inline=False)
            except discord.NotFound:
                embed.add_field(name='Невідомий користувач', value=birthday_str, inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def in_my_day(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        result = self.db.get_birthday(member.id)
        if not result:
            await ctx.send("День народження користувача не знайдений.")
            return

        birthday_str = result[0]
        birthday_date = datetime.datetime.strptime(birthday_str, '%Y-%m-%d').date()
        same_birthday_users = self.db.get_birthdays_by_date(birthday_date.strftime('%m-%d'))

        if not same_birthday_users:
            await ctx.send("Не знайдено користувачів з таким же днем народження.")
            return

        embed = discord.Embed(title=f"Список людей, в яких дн {birthday_date.strftime('%d.%m')}", color=0x00FF00)

        for result_user_id in same_birthday_users:
            result_user_id = result_user_id[0]
            if result_user_id != member.id:
                try:
                    user = await self.bot.fetch_user(result_user_id)
                    embed.add_field(name=user.display_name, value=birthday_date.strftime('%Y-%m-%d'), inline=False)
                except discord.NotFound:
                    embed.add_field(name="Невідомий користувач", value=birthday_date.strftime('%Y-%m-%d'), inline=False)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Birthdays(bot))
