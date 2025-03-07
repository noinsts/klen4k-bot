import sqlite3

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
            """CREATE TABLE IF NOT EXISTS birthday (
                user_id INTEGER PRIMARY KEY, 
                birthday TEXT
            )"""  # Додано закриваючу дужку
        )
        self.db.commit()


async def setup(bot):
    db = sqlite3.connect("birthdays.db")  # Створення з'єднання з БД
    cursor = db.cursor()  # Створення курсора
    await bot.add_cog(Birthdays(bot, db, cursor))