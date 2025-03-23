import random

import discord
from discord.ext import commands

from src.database import Database

class Chat(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.db = Database()


	@commands.hybrid_command(
		name = 'userinfo',
		description = 'Відображає інформацію про обраного користувача'
	)
	async def userinfo(self, ctx, member: discord.Member = None):
		member = member or ctx.author

		roles_name = [role.name for role in member.roles if role.name != '@everyone']  # пошук ролей користувача окрім '@everyone'
		role_text = ",\n ".join(roles_name) if roles_name else "Немає ролей"  # красивий вивід ролей

		color = discord.Color.blue()
		favourite_color = self.db.get_color(member.id)

		if favourite_color:
			color = int(favourite_color, 16)
			
		embed = discord.Embed(title=f'Інформація про користувача {member.name}', color = color)

		embed.add_field(name="👨🏻 Ім'я користувача", value=member.name, inline=False)
		embed.add_field(name='🤖 ID користувача', value=member.id, inline=False)
		embed.add_field(name='🎭 Ролі користувача', value=role_text, inline=False)

		balance = self.db.get_balance(member.id)
		privacy = self.db.get_balance_privacy(member.id)

		if balance and not privacy:
			embed.add_field(name='💸 Баланс користувача', value=f"⚠️ Заборгованість: {-balance} UAH" if balance < 0 else f"{balance} UAH", inline=False)

		city = self.db.get_city(member.id)
		country = self.db.get_country(member.id)

		if city and country:
			embed.add_field(name='🗺️ Місцезнаходження', value=f'{city}, {country}', inline=False)

		phone = self.db.get_phone(member.id)

		if phone:
			brand, model = phone
			embed.add_field(name='📱 Смартфон', value=f'{brand} {model}', inline=False)

		await ctx.send(embed=embed)


	@commands.hybrid_command(
		name = 'choice',
		description = 'Пропонує Так/Ні/Можливо, щодо вашого промпту'
	)
	async def choice(self, ctx, ask: str):
		answears = ["Так", "Ні", "Можливо"]
		await ctx.send(f'{random.choice(answears)}, {ask}')


	@commands.hybrid_command(
		name = 'who',
		description = 'Випадково обирає користувача',
		aliases=['кто', 'хто']
	)
	async def who(self, ctx, reason: str):
		member = random.choice(ctx.guild.members)
		 
		await ctx.send(f'**{member.mention}**, {reason}')


async def setup(bot):
	await bot.add_cog(Chat(bot))
