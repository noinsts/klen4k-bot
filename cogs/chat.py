import random

import discord
from discord.ext import commands

from database import Database

class Chat(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.db = Database()


	@commands.command()
	async def userinfo(self, ctx, member: discord.Member = None):
		member = member or ctx.author

		roles_name = [role.name for role in member.roles if role.name != '@everyone']  # пошук ролей користувача окрім '@everyone'
		role_text = ",\n ".join(roles_name) if roles_name else "Немає ролей"  # красивий вивід ролей

		embed = discord.Embed(title=f'Інформація про користувача {member.name}', color = discord.Color.blue())

		embed.add_field(name="Ім'я користувача", value=member.name, inline=False)
		embed.add_field(name='ID користувача', value=member.id, inline=False)
		embed.add_field(name='Ролі користувача', value=role_text, inline=False)

		balance = self.db.get_balance(member.id)
		privacy = self.db.get_balance_privacy(member.id)

		if balance and not privacy:
			embed.add_field(name='Баланс користувача', value=balance, inline=False)

		await ctx.send(embed=embed)


	@commands.command()
	async def choice(self, ctx, ask: str):
		answears = ["Так", "Ні", "Можливо"]
		await ctx.send(f'{random.choice(answears)}, {ask}')


	@commands.command(aliases=['кто', 'хто'])
	async def who(self, ctx, reason: str):
		member = random.choice(ctx.guild.members)
		 
		await ctx.send(f'**{member.mention}**, {reason}')


async def setup(bot):
	await bot.add_cog(Chat(bot))
