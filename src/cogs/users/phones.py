import discord
from discord.ext import commands

from ..base import BaseCog


class Phones(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)


    @commands.hybrid_command(
        name = 'add_phone',
        description = 'Додає ваш смартфон'
    )
    async def add_phone(self, ctx, brand: str, model: str):
        model_name = " ".join(model)
        if not brand or not model_name:
            await ctx.send('Помилка, введіть бренд та модель телефону')
            return
        
        if not self.db.phone.get_phone(ctx.author.id):
            self.db.phone.add_phone(ctx.author.id, brand, model_name)
            await ctx.send('Успіх! Ваш смартфон додано до бд')
        else:
            await ctx.send('Помилка! Ваш телефон вже є в бд')


    @commands.hybrid_command(
        name = 'edit_phone',
        description = 'Змінює ваш телефон'
    )
    async def edit_phone(self, ctx, brand: str, model: str):
        model_name = " ".join(model)
        if not brand or not model_name:
            await ctx.send('Помилка! Введіть нові бренд та модель смартфону')
            return
        
        if self.db.phone.get_phone(ctx.author.id):
            self.db.phone.edit_phone(ctx.author.id, brand, model_name)
            await ctx.send('Успіх! Ваш телефон оновлено.')
        else:
            await ctx.send('Помилка! Ваш телефон ще не вказаний, додайте його за допомогою **.add_phone**')


    @commands.hybrid_command(
        name = 'delete_phone',
        description = 'Видаляє ваш телефон'
    )
    async def delete_phone(self, ctx):
        if not self.db.phone.get_phone(ctx.author.id):
            await ctx.send('Помилка! Вашого телефону немає в базі')
            return
        
        self.db.phone.delete_phone(ctx.author.id)
        await ctx.send('Успіх! Ваш телефон видалено з бази.')


    @commands.hybrid_command(
        name = 'phone',
        description = 'Відображає смартфон обраного користувача'
    )
    async def phone(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        phone = self.db.phone.get_phone(member.id)

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
