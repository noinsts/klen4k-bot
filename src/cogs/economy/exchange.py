import requests
import discord
from discord.ext import commands

from src.cogs.base import BaseCog


class Exchange(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)


    @commands.hybrid_command(
        name='exchange',
        description='Відображає курс вибраної вами валюти'
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

        ISO_TO_CURRENCY = {840: 'USD', 978: 'EUR', 980: 'UAH'}

        CURRENCY_TO_ISO = {v: k for k, v in ISO_TO_CURRENCY.items()}

        emoji = {'USD': '🇺🇸', 'EUR': '🇪🇺', 'UAH': '🇺🇦'}

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

        embed = discord.Embed(title=f'Курс валют {emoji.get(ccy, "")} {ccy} -> {emoji.get(base_ccy, "")} {base_ccy}',
                              color=discord.Color.red())

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
    await bot.add_cog(Exchange(bot))
