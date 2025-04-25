import os
import random
from datetime import datetime

import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv

from src.cogs.base import BaseCog


class Weather(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)


    @staticmethod
    def api_key():
        load_dotenv()
        return os.getenv('WEATHER_API')


    @commands.hybrid_command(
        name = 'weather',
        description = 'Відправляє погоду по вказаному місту'
    )
    async def weather(self, ctx, city: str = None):
        if not city:
            saved_city = self.db.location.get_city(ctx.author.id)
            if saved_city:
                city = saved_city
            else:
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
            timezone_offset = data["timezone"]  # Часовий пояс у секундах
            sunrise = datetime.utcfromtimestamp(data["sys"]["sunrise"] + timezone_offset).strftime('%H:%M:%S')
            sunset = datetime.utcfromtimestamp(data["sys"]["sunset"] + timezone_offset).strftime('%H:%M:%S')


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

            weather_messages = {
                "clear sky": [
                    "Сонце світить, пташки співають! Час для прогулянки! 🌞",
                    "Чисте небо – ідеальний день для активностей! 🚴‍♂️",
                    "Окуляри не забудь 😎"
                ],
                "few clouds": [
                    "Трохи хмар, але загалом чудово! 🌤️",
                    "Сонце визирає – гарний день для кави на вулиці ☕",
                    "Кілька хмаринок не завадять гарному настрою!"
                ],
                "rain": [
                    "Дощить? Саме час для гарячого чаю і фільму! 🎬☕",
                    "Якщо виходиш – не забудь парасольку! ☂️",
                    "Парасолька головний аксесуар дня!"
                ],
                "snow": [
                    "Сніг летить? Вийди і зліпи сніговика! ⛄",
                    "Ідеальний момент для гарячого шоколаду ☕",
                    "Нарешті справжня зима! ❄️"
                ],
                "thunderstorm": [
                    "Гримить і блискає! Тримайся подалі від відкритих місць! ⚡",
                    "Якщо чуєш гуркіт – це не сабвуфер сусіда! 😆",
                    "Гроза – найкращий час для атмосфери і свічок 🕯️"
                    
                ],
                "overcast clouds": [
                    "Сіренько, але без дощу. Саме час для кави ☕", 
                    "Може здатися похмуро, але це не привід сидіти вдома!"
                ]
            }

            translate_desc, embed_color = weather_descriptions.get(desc, (desc, discord.Color.blue()))

            advice = random.choice(weather_messages.get(desc, ["Немає особливих рекомендацій 🤷"]))

            embed = discord.Embed(title=f'Прогноз погоди в {city}, {country}', color=embed_color)

            embed.add_field(name='Температура', value=f'{temp}°C', inline=False)
            embed.add_field(name='Вологість', value=f'{humid}%', inline=False)
            embed.add_field(name='Опис', value=translate_desc, inline=False)
            embed.add_field(name='🌄 Схід сонця', value=sunrise, inline=True)
            embed.add_field(name='🌇 Захід сонця', value=sunset, inline=True)
            embed.add_field(name='🔮 Порада', value=advice, inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send("Помилка, невдалося встановити підключення з сервером")
            return
        

    @commands.hybrid_command(
        name = 'set_location',
        description = 'Встановлює ваше місто',
        aliases=['add_location']
    )
    async def set_location(self, ctx, city: str, country: str):
        if not city:
            await ctx.send('Помилка! Ви не вказали місто.')
            return
        
        if not country:
            await ctx.send('Помилка! Ви не вказали країну')
            return
        
        if self.db.location.get_city(ctx.author.id):
            await ctx.send('Помилка! Данні про місто та країну вже додані')
        else:
            self.db.location.add_location(ctx.author.id, city, country)
            await ctx.send(f"Успіх! Вашу локацію **{city}** та **{country}** додано до бд.")


    @commands.hybrid_command(
        name = 'change_location',
        description = 'Змінює ваше місто'
    )
    async def change_location(self, ctx, city: str, country: str):
        if not city:
            await ctx.send('Помилка! Ви не вказали місто.')
            return

        if not country:
            await ctx.send('Помилка! Ви не вказали країну')
            return
        
        self.db.location.edit_location(ctx.author.id, city, country)
        await ctx.send('Успіх! Ви змінили назву ваших міста та країни в бд.')


    @commands.hybrid_command(
        name = 'del_location',
        description = 'Видає ваше місто',
        alises=['delete_location']
    )
    async def del_location(self, ctx):
        self.db.location.delete_location(ctx.author.id)
        await ctx.send('Успіх! Ви видалили вашу локацію з бд.')

    def find_weather_type(self, city):
        base_url = 'http://api.openweathermap.org/data/2.5/weather'
        api_key = self.api_key()

        params = {
            "q" : city,
            "appid" : api_key
        }

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()

            type = data['weather'][0]['description']

            POSITIVE_WEATHER = {"clear sky", "few clouds", "scattered clouds", "broken clouds", "mist"}
            NEGATIVE_WEATHER = {"overcast clouds", "drizzle", "rain", "thunderstorm", "snow", "haze", 
                                "fog", "sand", "dust", "ash", "squall", "tornado"}
            
            if type in POSITIVE_WEATHER:
                return 'positive'
            elif type in NEGATIVE_WEATHER:
                return 'negative'
            else:
                return 'neutral'


    @commands.hybrid_command(
        name = 'add_weahter_advice',
        description = 'Додає персоналізовану пораду'
    )
    async def add_weather_advice(self, ctx, weather_type: str, *, activity: str): 
        if weather_type not in ['positive', 'negative']:
            await ctx.send('Помилка! Використовуйте **positive** або **negative**')
            return
        
        self.db.location.add_advice(ctx.author.id, weather_type, activity)
        await ctx.send('Успіх! Ваші персоналізовані поради додано.')


    @commands.hybrid_command(
        name = 'personalize_advice',
        description = 'Пропонує вам персоналізовану пораду'
    )
    async def personalize_advice(self, ctx):
        city = self.db.location.get_city(ctx.author.id)
        weather = self.find_weather_type(city)
        activities = self.db.location.find_advice(ctx.author.id, weather)

        if not city:
            await ctx.send('Ви не вказали місто, спробуйте **.add_location**')

        if not activities:
            await ctx.send('Немає персоналізованих активностей. Ви можете їх додати, використовуючи **.add_weather_advice**.')
            return

        if weather == 'positive':
            emoji = '🌄'
            color = discord.Color.orange()
        else:
            emoji = '🌙'
            color = discord.Color.blue()

        embed = discord.Embed(
            title=f'𝒀𝒐𝒖𝒓 𝒑𝒆𝒓𝒔𝒐𝒏𝒂𝒍𝒊𝒛𝒆 𝒂𝒅𝒗𝒊𝒄𝒆 {emoji}', 
            description=random.choice(activities)[0],
            color=color
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Weather(bot))
