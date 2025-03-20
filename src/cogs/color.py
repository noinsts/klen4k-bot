from discord.ext import commands

from src.database import Database


class Color(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()


    @commands.command()
    async def add_color(self, ctx, color: str):
        if self.db.add_color(ctx.author.id, color):
            await ctx.send('Успіх! Ваш улюблений колір додано')
        else:
            await ctx.send("Помилка, некоректний HEX-код, введіть щось типу '#ff0000'.")

    @commands.command()
    async def edit_color(self, ctx, color: str):
        if self.db.edit_color(ctx.author.id, color):
            await ctx.send('Успіх! Колір змінено')
        else:
            await ctx.send("Помилка, некоректний HEX-код, введіть щось типу '#ff0000'.")

    @commands.command()
    async def delete_color(self, ctx):
        if self.db.delete_color(ctx.author.id):
            await ctx.send('Успіх! Колір видалено з бд')
        else:
            await ctx.send("Помилка, колір не видалено, спробуйте знову")


async def setup(bot):
    await bot.add_cog(Color(bot))
    