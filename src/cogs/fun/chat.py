import random

import discord
from discord.ext import commands

from ..base import BaseCog

class Chat(BaseCog):
	def __init__(self, bot):
		super().__init__(bot)


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
