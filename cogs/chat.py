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
	async def random(self, ctx):
		voice = ctx.author.voice
		channel = voice.channel
		members = channel.members
		members_names = [member.display_name for member in members]

		random.shuffle(members_names)

		team1 = members_names[:2]
		team2 = members_names[2:]

		embed = discord.Embed(title='Розподіл команд', color=discord.Color.red())

		embed.add_field(name='Команда 1', value=f", \n".join(team1), inline=True)
		embed.add_field(name='Команда 2', value=f", \n".join(team2), inline=True)

		if not voice and not voice.channel:
			await ctx.send('Щоб використовувати цю команду зайдіть в войс')
		elif len(members) != 4:
			await ctx.send('Що використовувати цю команду потрібно щоб в войсі було 4 людини')
		else:
			await ctx.send(embed=embed)


async def setup(bot):
	await bot.add_cog(Chat(bot))
