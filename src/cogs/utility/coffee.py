import discord
from discord import Interaction
from discord.ext import commands
from discord.ui import View, Button

from src.cogs.base import BaseCog


class Coffee(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)


    @commands.hybrid_command(
        name = 'coffee_menu',
        description = 'Меню всіх кав'
    )
    async def coffee_menu(self, ctx):
        await ctx.send('Вибери свою каву', view=CoffeeView())


class CoffeeView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Словник з інформацією про каву, де ключі - це українські назви кав
        self.coffee_info = {
            "Еспресо": "Еспресо – це міцна та насичена кава, яка готується під високим тиском. Ідеальний вибір для тих, хто любить чистий смак кави!",
            "Капучино": "Капучіно – це класичний напій з еспресо, молоком і ніжною пінкою. Баланс міцності та ніжності!",
            "Латте": "Лате – це м'яка та молочна кава з еспресо. Чудовий вибір для тих, хто любить солодкуватий і кремовий смак!",
            "Раф": "Раф – це ніжна кава з вершками та ванільним цукром. Має кремову текстуру і солодкий смак!",
            "Американо": "Американо – це еспресо, розведене гарячою водою. Більш м'який, ніж еспресо, але з тим же ароматом!",
            "Допіо": "Допіо – це подвійний еспресо. У два рази більше енергії та смаку для справжніх любителів кави!",
            "Макіато": "Макіато – це еспресо з невеликою кількістю молочної пінки. Зберігає міцний смак з легким молочним відтінком!",
            "Флет-вайт": "Флет-вайт – це еспресо з тонким шаром мікропіни. Схоже на лате, але з більш виразним смаком кави!"
        }

        self.coffee_names = list(self.coffee_info.keys())

        for coffee in self.coffee_names:
            self.add_item(Button(label=coffee + " ☕", style=discord.ButtonStyle.primary, custom_id=coffee))


    async def interaction_check(self, interaction: Interaction, /) -> bool:
        coffee_type = interaction.data['custom_id']
        await interaction.response.send_message(f"Готуємо {coffee_type}... ☕\n{self.coffee_info[coffee_type]}", ephemeral=True)
        return True


async def setup(bot):
    await bot.add_cog(Coffee(bot))
