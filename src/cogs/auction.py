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

        self.db.add_auc_item(ctx.author.id, name)
        auc_id = self.db.get_auction_id(ctx.author.id, name)
        await ctx.send(f'Успіх! Ви додали лот **{name}**, його ID: **{auc_id}**')


    @commands.hybrid_command(
        name='auction',
        description = 'Бот відправляє список активних лотів'
    )
    async def auction(self, ctx):
        results = self.db.auc_list()

        if not results:
            await ctx.send("Немає активних лотів")
            return
        
        embed = discord.Embed(title='Список активних лотів', color=discord.Color.blue())

        for id, user_id, name in results:
            user = await self.bot.fetch_user(user_id)
            title = f'(#{id}) від {user.display_name}'
            embed.add_field(name=title, value=name, inline=False)

        await ctx.send(embed=embed)


    @commands.hybrid_command(
        name='my_auc',
        description = 'Відображає список ваших замовлень'
    )
    async def my_auc(self, ctx: commands.Context, user: discord.Member = None):
        user = user if user else ctx.author 
        user_id = user.id

        results = self.db.user_auc_list(user_id)

        if not results:
            await ctx.send(f'У користувача **{user.display_name}** немає активних лотів')
            return

        embed = discord.Embed(title=f'Список лотів користувача {user.display_name}', color=discord.Color.blue())

        for id, name in results:
            embed.add_field(name=f'Лот №{id}', value=name, inline=False)

        await ctx.send(embed=embed)


    @commands.hybrid_command(
        name = 'close_auc',
        description = 'Інстумент за допомогою якого можна закрить заявку на аукціоні'
    )
    async def close_auc(self, ctx, id_auc: int):
        if not id_auc:
            await ctx.send("Помилка! Ви не вказали id")
            return
        
        if self.db.delete_auc(id_auc, ctx.author.id):
            await ctx.send(f'Успіх! Лот **№{id_auc}** видалено.')
        else:
            await ctx.send('Помилка. Видалити лот не вдалося')


async def setup(bot):
    await bot.add_cog(Auction(bot))
