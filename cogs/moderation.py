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


	@commands.command()
	@commands.has_permissions(administrator = True)
	async def nickname(self, ctx, member: discord.Member, newnick: str):
		if newnick is None:
			await member.edit(nick=None)
			await ctx.send(f'Нікнейм скинуто для користувача **{member.display_name}**')
		else:
			await member.edit(nick=newnick)
			await ctx.send(f'Нік **{newnick}** для користувача **{member.display_name}** встановлено')



	@commands.command()
	@commands.has_permissions(administrator = True)
	async def vacban(self, ctx, member: discord.Member, reason: str = None):
		await member.ban(reason=reason)
		await ctx.send(f'Користувач **{member.display_name}** був заблокований за причини **{reason}** користувачем {ctx.author.display_name}')


	@commands.command()
	@commands.has_permissions(administrator = True)
	async def mute(self, ctx, member: discord.Member):
		await member.edit(mute=True)
		await ctx.send(f'Користувач **{member.display_name}** замучений у войсі')


	@commands.command()
	@commands.has_permissions(administrator = True)
	async def unmute(self, ctx, member: discord.Member):
		await member.edit(mute=False)
		await ctx.send(f'Користувач **{member.display_name}** розмучений у войсі')


	@commands.command()
	@commands.has_permissions(administrator = True)
	async def deafen(self, ctx, member: discord.Member):
		await member.edit(deafen=True)
		await ctx.send(f'Користувач **{member.display_name}** заглушений у войсі')


	@commands.command()
	@commands.has_permissions(administrator = True)
	async def undeafen(self, ctx, member: discord.Member):
		await member.edit(deafen=False)
		await ctx.send(f'Користувач **{member.display_name}** розглушений у войсі')


async def setup(bot):
	await bot.add_cog(Moderation(bot))
