import os

import requests

import discord
from discord.ext import commands

from src.database import Database

from dotenv import load_dotenv


class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()


    @commands.hybrid_command(
        name = 'change_balance',
        description = 'Змінює баланс вказаного користувача (тільки адміністратор)'
    )
    @commands.has_permissions(administrator=True)
    async def change_balance(self, ctx, amount: int, member: discord.Member = None):
        if not member:
            member = ctx.author

        if amount == 0:
            await ctx.send(f'Баланс користувача **{member.display_name}** не змінено.')
            return

        self.db.update_balance(member.id, amount)  # запит на зміну балансу

        if amount > 0:
            await ctx.send(f'Баланс користувача **{member.display_name}** збільшено на **{amount}** 💸')
        else:
            await ctx.send(f'Баланс користувача **{member.display_name}** зменшено на **{-amount}** 💸')


    @commands.hybrid_command(
        name = 'balance',
        description = 'Відображає ваш баланс'
    )
    async def balance(self, ctx, member: discord.Member = None):
        if not member:
            balance = self.db.get_balance(ctx.author.id)
            await ctx.send(f'Ваш баланс **{balance}** гривень 💸')
        else:
            balance = self.db.get_balance(member.id)
            await ctx.send(f'Баланс користувача **{member.display_name}** **{balance}** гривень 💸')


    @commands.hybrid_command(
        name = 'balance_tier_list',
        description = 'Список мажорів серверу'
    )
    async def balance_tier_list(self, ctx):
        result = self.db.balance_tier_list()
        
        if not result:
            await ctx.send('Інформації не знайдено, спробуйте пізніше')
            return
        
        embed = discord.Embed(title='Тір-ліст за балансом', color=discord.Color.gold())

        medals = ['🥇', '🥈', '🥉']
        for index, (user_id, balance) in enumerate(result, start=1):
            user = ctx.guild.get_member(user_id)
            if user:
                medal = medals[index - 1] if index <= 3 else f'{index}'
                embed.add_field(name=f'{medal} **{user.display_name}**', value = f'{balance}$', inline=False)
        await ctx.send(embed=embed)


    @commands.command()
    # залишаємо без змін
    @commands.has_permissions(administrator = True)
    async def clear_balances(self, ctx, password: str):
        if not password:
            await ctx.send('Введіть пароль')
            return

        load_dotenv()
        correct = os.getenv('PASSWORD')

        if password != correct:
            await ctx.send('Введіть правильний пароль')
            return
        
        self.db.clear_balances()

        await ctx.send('**BALANCES DATABASE IS CLEAR**')


    @commands.hybrid_command(
        name = 'balance_privacy',
        description = 'Дозволяє змінити налаштування приватності вашого балансу'
    )
    async def balance_privacy(self, ctx):
        state = 1 if not self.db.get_balance_privacy(ctx.author.id) else 0
        self.db.set_balance_privacy(state, ctx.author.id)
        await ctx.send(f'Статус приватності балансу змінено на **{bool(state)}**')


    @commands.hybrid_command(
        name = 'exchange',
        description = 'Відображає курс вибраної вами валюти'
    )
    async def exchange(self, ctx, ccy: str, base_ccy: str, money: int = None):
        if not base_ccy or not ccy:
            await ctx.send('Ви не вказали валюту')
            return
        
        url = "https://api.monobank.ua/bank/currency"
        response = requests.get(url)
        
        try:
            data = response.json()
        except ValueError:
            await ctx.send("❌ Помилка отримання курсу валют.")
            return

        if not isinstance(data, list):
            await ctx.send("❌ Невірний формат відповіді від API.")
            return

        ISO_TO_CURRENCY = {840: 'USD', 978: 'EUR', 980 : 'UAH'}

        CURRENCY_TO_ISO = {v: k for k, v in ISO_TO_CURRENCY.items()}

        emoji = {'USD' : '🇺🇸', 'EUR' : '🇪🇺', 'UAH' : '🇺🇦'}

        if ccy not in CURRENCY_TO_ISO or base_ccy not in CURRENCY_TO_ISO:
            await ctx.send('Вибачте, ваша валюта не підтримується')
            return
        
        from_iso = CURRENCY_TO_ISO[ccy]
        to_iso = CURRENCY_TO_ISO[base_ccy]

        direct_rate_buy = None
        direct_rate_sell = None

        for currency in data:
            if currency['currencyCodeA'] == from_iso and currency['currencyCodeB'] == to_iso:
                direct_rate_buy = currency.get('rateBuy')
                direct_rate_sell = currency.get('rateSell')
                break

        embed = discord.Embed(title=f'Курс валют {emoji.get(ccy, "")} {ccy} -> {emoji.get(base_ccy, "")} {base_ccy}', color=discord.Color.red())

        if direct_rate_buy and direct_rate_sell:
            embed.add_field(name='Купівля', value=direct_rate_buy, inline=False)
            embed.add_field(name='Продаж', value=direct_rate_sell, inline=False)

            if money:
                convert = money * direct_rate_sell
                embed.add_field(name='Ви отримаєте', value=f'{money} {ccy} ≈ {convert:.2f} {base_ccy}', inline=False)

            await ctx.send(embed=embed)
            return
        
        if (from_iso == 980 and to_iso == 978) or (from_iso == 978 and to_iso == 980):  # UAH <-> EUR
            usd_to_uah = next((c for c in data if c["currencyCodeA"] == 840 and c["currencyCodeB"] == 980), None)
            eur_to_usd = next((c for c in data if c["currencyCodeA"] == 978 and c["currencyCodeB"] == 840), None)

            if usd_to_uah and eur_to_usd:
                rate_buy = eur_to_usd["rateBuy"] * usd_to_uah["rateBuy"]
                rate_sell = eur_to_usd["rateSell"] * usd_to_uah["rateSell"]

                embed.add_field(name='Купівля', value=f'{rate_buy:.4f}', inline=False)
                embed.add_field(name='Продаж', value=f'{rate_sell:.4f}', inline=False)

                if money:
                    convert = money / rate_sell
                    embed.add_field(name='Ви отримаєте:', value=f'{money} {ccy} ≈ {convert:.2f} {base_ccy}')

            await ctx.send(embed=embed)
            return
        
        await ctx.send('Помилка, нічого не знайдено')

async def setup(bot):
    await bot.add_cog(Balance(bot))
