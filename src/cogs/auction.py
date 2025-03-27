import discord
from discord.ext import commands

from src.database import Database


class Auction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()


    @commands.hybrid_command(
        name='add_item',
        description = 'Додає замовлення в Minecraft до списку замовлень'
    )
    async def add_item(self, ctx, *, name: str):
        if not name:
            await ctx.send('Введіть назву предмету, що потрібно замовити')
            return

        """
        TODO: створити функцію додавання предмету до аукціону
        після цього відобразити номер заявки
        """

        pass


    @commands.hybrid_command(
        name='auction',
        description = ''
    )
    async def auction(self, ctx):
        """
        TODO: створити список предметів аукціону
        """

        pass


    @commands.hybrid_command(
        name='my_auc',
        descriptio = 'Відображає список ваших замовлень'
    )
    async def my_auc(self, ctx):

        """
        TODO: повернути список ваших замовлень з номером заявки
        """

        pass


    @commands.hybrid_command(
        name = 'close_auc',
        description = 'Інстумент за допомогою якого можна закрить заявку на аукціоні'
    )
    async def close_auc(self, ctx, id_auc: int):
        """
        TODO: за введеним користувачес id видалити з бд колонку
        """

        pass


async def setup(bot):
    await bot.add_cog(Auction(bot))
