import random

import discord
from discord.ext import commands

from ..base import BaseCog


class Teams(BaseCog):
	def __init__(self, bot):
		super().__init__(bot)


	@commands.hybrid_command(
		name = 'teams_create',
		description = 'Створює команду (розподіляє 4 учасників войсу на 2 команди)'
	)
	async def teams_create(self, ctx):
		voice = ctx.author.voice
		channel = voice.channel
		members = channel.members
		members_names = [member.display_name for member in members]

		random.shuffle(members_names)

		team1 = members_names[:2]
		team2 = members_names[2:]

		team1_role = ctx.guild.get_role(cfg.TEAM_1_ID)
		team2_role = ctx.guild.get_role(cfg.TEAM_2_ID)

		if not team1_role or not team2_role:
			await ctx.send('Не знайдено ролі команд. Переконайтеся, що ID ролей правильні.')
			return

		embed = discord.Embed(title='Розподіл команд', color=discord.Color.red())

		embed.add_field(name='Команда 1', value=f", \n".join(team1), inline=True)
		embed.add_field(name='Команда 2', value=f", \n".join(team2), inline=True)

		if not voice and not voice.channel:
			await ctx.send('Щоб використовувати цю команду зайдіть в войс')
		elif len(members) != 4:
			await ctx.send('Що використовувати цю команду потрібно щоб в войсі було 4 людини')
		else:
			for member in team1:
				await member.add_roles(cfg.TEAM_1_ID)

			for member in team2:
				await member.add_roles(cfg.TEAM_2_ID)

			await ctx.send(embed=embed)


	@commands.hybrid_command(
		name = 'clear_teams',
		description = 'Видаляє ролі команд в учасників серверу'
	)
	async def clear_teams(self, ctx):
		for role_id in [cfg.TEAM_1_ID, cfg.TEAM_2_ID]:
			role = ctx.guild.get_role(role_id)
			if role:
				for member in role.members:
					await member.remove_roles(role)
			await ctx.send("Ролі команд очищено!")


	@commands.hybrid_command(
		name = 'teamsplit',
		description = 'Розподіляє учасників по войсах'
	)
	async def teamsplit(self, ctx):
		team1_members = ctx.guild.get_role(cfg.TEAM_1_ID).members
		team2_members = ctx.guild.get_role(cfg.TEAM_2_ID).members

		team_A = ctx.guild.get_channel(cfg.TEAM_A_ID)  # войс команди 1
		team_B = ctx.guild.get_channel(cfg.TEAM_B_ID)  # войс команди 2

		for member in team1_members:
			await member.move_to(team_A)

		for member in team2_members:
			await member.move_to(team_B)

		await ctx.send('Учасники розкинуті по войсах')


	@commands.hybrid_command(
		name = 'teammerge',
		description = "З'єднує команди в один войс"
	)
	async def teammerge(self, ctx):
		team1_members = ctx.guild.get_role(cfg.TEAM_1_ID).members
		team2_members = ctx.guild.get_role(cfg.TEAM_2_ID).members

		all_team_members = team1_members + team2_members

		full_stack = ctx.guild.get_channel(cfg.FULL_STACK_ID)  # войс загального збору

		for member in all_team_members:
			await member.move_to(full_stack)

		await ctx.send(f'Всі учасники повернуті в **{full_stack.name}**')


async def setup(bot):
	await bot.add_cog(Teams(bot))
