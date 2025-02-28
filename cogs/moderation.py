import discord
from discord.ext import commands
from datetime import timedelta


class Moderation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command()
	@commands.has_permissions(administrator = True)
	async def timeout(self, ctx, member: discord.Member, time: int, *, reason='Не вказано'):
		duration = discord.utils.utcnow() + timedelta(minutes=time)
		await member.timeout(duration, reason=reason)
		await ctx.send(f"Користувач **{member}** тимчасово заблокований на **{time}** хвилин. Причина: **{reason}**")


	@commands.command()
	@commands.has_permissions(administrator = True)
	async def untimeout(self, ctx, member: discord.Member):
		await member.timeout(None)
		await ctx.send(f"Користувач **{member}** розблокований")


async def setup(bot):
	await bot.add_cog(Moderation(bot))

