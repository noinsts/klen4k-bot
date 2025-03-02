import random

import discord
from discord.ext import commands

import config as cfg


class Chat(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command()
	async def userinfo(self, ctx, member: discord.Member = None):
		guild = self.bot.get_guild(cfg.GUILD_ID)
		member = member or ctx.author

		roles_name = [role.name for role in member.roles if role.name != '@everyone']
		role_text = ",\n ".join(roles_name) if roles_name else "Немає ролей"

		embed = discord.Embed(title=f'Інформація про користувача {member.name}', color = discord.Color.blue())

		embed.add_field(name="Ім'я користувача", value=member.name, inline=True)
		embed.add_field(name='ID користувача', value=member.id, inline=True)
		embed.add_field(name='Ролі користувача', value=role_text, inline=True)

		await ctx.send(embed=embed)


	@commands.command()
	async def choice(self, ctx, ask: str):
		answears = ["Так", "Ні", "Можливо"]
		answear = random.choice(answears)

		await ctx.send(f'{answear}, {ask}')


	@commands.command(aliases=['кто', 'хто'])
	async def who(self, ctx, reason: str):
		 member = random.choice(ctx.guild.members)
		 
		 await ctx.send(f'**{member.mention}**, {reason}')


async def setup(bot):
	await bot.add_cog(Chat(bot))
