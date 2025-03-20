import discord
from discord.ext import commands

from src import config as cfg

from src.database import Database


class Taxes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()


    @commands.command()
    @commands.has_permissions(administrator = True)
    async def toggle_taxes(self, ctx):
        state = 1 if not self.db.get_tax_state() else 0
        self.db.set_tax_state(state)
        await ctx.send(f"Податки {'увімкнено' if state else 'вимкнено'}!")


    @commands.command()
    @commands.has_permissions(administrator = True)
    async def change_tax(self, ctx, action: str, amount: int):
        self.db.set_taxes(action, amount)
        await ctx.send('Податок змінено')

    @commands.command()
    async def taxes(self, ctx):
        taxes = self.db.get_taxes()
        allow = self.db.get_tax_state()

        if not taxes:
            await ctx.send('Немає категорій податків')
            return
        
        embed = discord.Embed(title='Податки', color=16777215)

        if allow:
            embed.add_field(name='**⚠️ Статус**', value='**Наразі податки ввімкнено**', inline=False)
        else:
            embed.add_field(name='**⚠️ Статус**', value='**Наразі податки вимкнено**')

        for name, amount in taxes:
            embed.add_field(name=name, value=f'{amount} ', inline=False)

        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            if self.db.get_tax_state():
                tax = self.db.amount_tax("join_voice")  # змінено на "join_voice"

                if not tax:
                    print("Помилка: податок для 'join_voice' не знайдено в БД!")
                    return

                self.db.update_balance(member.id, -tax)

                if self.db.is_log_allowed("tax_logs"):
                    log_channel = member.guild.get_channel(cfg.LOG_CHANNEL_ID)

                    if log_channel:
                        embed = discord.Embed(
                            title='Новий податок!',
                            description=f'**{member.display_name}** зайшов у войс, з нього знято {tax} грошей',
                            color=discord.Color.red()
                        )
                        await log_channel.send(embed=embed)


    """SHOW/HIDE TAX LOGS LOCATED IN logs.py"""



async def setup(bot):
    await bot.add_cog(Taxes(bot))
