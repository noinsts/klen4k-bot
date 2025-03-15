import os

import requests

from dotenv import load_dotenv

import discord
from discord.ext import commands


class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    def api_key(self):
        load_dotenv()
        return os.getenv('WEATHER_API')

    
    @commands.command()
    async def weather(self, ctx, city: str):
        if not city:
            await ctx.send('Введіть назву міста')
            return
        
        base_url = 'http://api.openweathermap.org/data/2.5/weather'
        api_key = self.api_key()

        params = {
            "q" : city,
            "appid" : api_key,
            "units" : "metric"
        }

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()

            temp = data['main']['temp']
            humid = data['main']['humidity']
            desc = data['weather'][0]['description']
            city = data['name']
            country = f':flag_{data['sys']['country'].lower()}:'


            weather_descriptions = {
                "clear sky": ("Ясне небо ☀️", 0xFFFF00),  # Жовтий для ясного неба
                "few clouds": ("Мало хмар ️", 0xADD8E6),  # Світло-синій для малої хмарності
                "scattered clouds": ("Розкидані хмари ⛅", 0x87CEEB),  # Синій для розкиданих хмар
                "broken clouds": ("Розірвані хмари ☁️", 0x778899),  # Сірий для розірваних хмар
                "shower rain": ("Злива ️", 0x1E90FF),  # Синій для зливи
                "rain": ("Дощ ☔", 0x4169E1),  # Темно-синій для дощу
                "thunderstorm": ("Гроза ⛈️", 0x800080),  # Фіолетовий для грози
                "snow": ("Сніг ❄️", 0xFFFFFF),  # Білий для снігу
                "mist": ("Туман ️", 0xD3D3D3),  # Світло-сірий для туману
                "overcast clouds": ("Хмарно ☁️", 0xA9A9A9)  # Темно-сірий для хмарності
            }

            translate_desc, embed_color = weather_descriptions.get(desc, (desc, discord.Color.blue()))

            embed = discord.Embed(title=f'Прогноз погоди в {city}, {country}', color=embed_color)

            embed.add_field(name='Температура', value=f'{temp}°C', inline=False)
            embed.add_field(name='Вологість', value=f'{humid}%', inline=False)
            embed.add_field(name='Опис', value=translate_desc, inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send("Помилка, невдалося встановити підключення з сервером")
            return


async def setup(bot):
    await bot.add_cog(Weather(bot))