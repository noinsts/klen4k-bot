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


async def setup(bot):
    db = sqlite3.connect("birthdays.db")  # Створення з'єднання з БД
    cursor = db.cursor()  # Створення курсора
    await bot.add_cog(Birthdays(bot, db, cursor))