import sqlite3

import datetime

import discord
from discord.ext import commands


class Birthdays(commands.Cog):
    def __init__(self, bot, db, cursor):
        self.bot = bot
        self.db = db
        self.cursor = cursor
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS birthdays (
                user_id INTEGER PRIMARY KEY, 
                birthday TEXT
            )"""  # Додано закриваючу дужку
        )
        self.db.commit()


    @commands.command()
    async def add_birthday(self, ctx, date: str, member: discord.Member = None):
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            await ctx.send("Невірний формат дати, спробуйте YYYY-MM-DD")
            return

        if member is None:
            member = ctx.author

        user_id = member.id
        self.cursor.execute("INSERT OR REPLACE INTO birthdays VALUES (?, ?)", (user_id, date))
        self.db.commit()
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

        user_id = member.id

        self.cursor.execute("UPDATE birthdays SET birthday = ? WHERE user_id = ?", (date, user_id))
        self.db.commit()
        await ctx.send(f'Дата народження користувача **{member.display_name}** оновлена до **{date}**')


    @commands.command()
    async def remove_birthday(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        user_id = member.id

        self.cursor.execute("DELETE FROM birthdays WHERE user_id = ?", (user_id, ))
        self.db.commit()
        await ctx.send(f'Дата народження користувача **{member.display_name}** видалено')


    @commands.command()
    async def birthday(self, ctx, member: discord.Member = None):
        author = None

        if member is None:
            member = ctx.author
            author = True

        user_id = member.id

        self.cursor.execute("SELECT birthday FROM birthdays WHERE user_id = ?", (user_id, ))
        result = self.cursor.fetchone()

        if result:
            send = result[0]
            if author:
                await ctx.send(f'Ваш день народження **{send}**')
            else:
                await ctx.send(f'День народження користувача **{member.display_name}** **{send}**')



    @commands.command()
    async def birthday_list(self, ctx):
        self.cursor.execute("SELECT user_id, birthday FROM birthdays")
        results = self.cursor.fetchall()

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

        user_id = member.id

        # Отримуємо день народження користувача
        self.cursor.execute("SELECT birthday FROM birthdays WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()

        if not result:
            await ctx.send("День народження користувача не знайдений.")
            return

        birthday_str = result[0]
        birthday_date = datetime.datetime.strptime(birthday_str, '%Y-%m-%d').date()

        # Знаходимо всіх користувачів з таким же днем народження
        self.cursor.execute("SELECT user_id FROM birthdays WHERE strftime('%m-%d', birthday) = ?", (birthday_date.strftime('%m-%d'),))
        results = self.cursor.fetchall()

        if not results:
            await ctx.send("Не знайдено користувачів з таким же днем народження.")
            return

        embed = discord.Embed(title=f"Список людей, в яких дн {birthday_date.strftime('%d.%m')}", color=0x00FF00)

        for result_user_id in results:
            result_user_id = result_user_id[0]
            if result_user_id != user_id:  # Виключаємо самого користувача
                try:
                    user = await self.bot.fetch_user(result_user_id)
                    embed.add_field(name=user.display_name, value=birthday_date.strftime('%Y-%m-%d'), inline=False)
                except discord.NotFound:
                    embed.add_field(name="Невідомий користувач", value=birthday_date.strftime('%Y-%m-%d'), inline=False)

        await ctx.send(embed=embed)


    @commands.command()
    async def come_birthday(self, ctx):
        pass


async def setup(bot):
    db = sqlite3.connect("birthdays.db")  # Створення з'єднання з БД
    cursor = db.cursor()  # Створення курсора
    await bot.add_cog(Birthdays(bot, db, cursor))
