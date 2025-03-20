import discord
from discord.ext import commands

from src.database import Database


class Phones(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    @commands.command()
    async def add_phone(self, ctx, brand: str, *model: str):
        model_name = " ".join(model)
        if not brand or not model_name:
            await ctx.send('Помилка, введіть бренд та модель телефону')
            return
        
        if not self.db.get_phone(ctx.author.id):
            self.db.add_phone(ctx.author.id, brand, model_name)
            await ctx.send('Успіх! Ваш смартфон додано до бд')
        else:
            await ctx.send('Помилка! Ваш телефон вже є в бд')

    @commands.command()
    async def edit_phone(self, ctx, brand: str, *model: str):
        model_name = " ".join(model)
        if not brand or not model_name:
            await ctx.send('Помилка! Введіть нові бренд та модель смартфону')
            return
        
        if self.db.get_phone(ctx.author.id):
            self.db.edit_phone(ctx.author.id, brand, model_name)
            await ctx.send('Успіх! Ваш телефон оновлено.')
        else:
            await ctx.send('Помилка! Ваш телефон ще не вказаний, додайте його за допомогою **.add_phone**')


    @commands.command()
    async def delete_phone(self, ctx):
        if not self.db.get_phone(ctx.author.id):
            await ctx.send('Помилка! Вашого телефону немає в базі')
            return
        
        self.db.delete_phone(ctx.author.id)
        await ctx.send('Успіх! Ваш телефон видалено з бази.')


    @commands.command()
    async def phone(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        phone = self.db.get_phone(member.id)

        embed = discord.Embed(title=f'Смартфон користувача {member.display_name}', color=0x808080)

        if phone:
            brand, model = phone
            embed.add_field(name='Бренд', value=brand, inline=False)
            embed.add_field(name='Модель', value=model, inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send('Помилка! Ваш телефон ще не вказаний, додайте його за допомогою **.add_phone**')


async def setup(bot):
    await bot.add_cog(Phones(bot))
