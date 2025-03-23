import asyncio
import discord
from discord.ext import commands
from datetime import timedelta


class Moderation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.hybrid_command(
		name="timeout",
		description="Тимчасово блокує користувача."
	)
	@commands.has_permissions(administrator=True)
	async def timeout(self, ctx, member: discord.Member, time: int, *, reason='Не вказано'):
		duration = discord.utils.utcnow() + timedelta(minutes=time)
		await member.timeout(duration, reason=reason)
		await ctx.send(
			f"Користувач **{member}** тимчасово заблокований на **{time}** хвилин. Причина: **{reason}**")


	@commands.hybrid_command(
		name="untimeout",
		description="Розблоковує користувача."
	)
	@commands.has_permissions(administrator=True)
	async def untimeout(self, ctx, member: discord.Member):
		await member.timeout(None)
		await ctx.send(f"Користувач **{member}** розблокований")


	@commands.hybrid_command(
		name="nickname",
		description="Змінює нікнейм користувача."
	)
	@commands.has_permissions(administrator=True)
	async def nickname(self, ctx, member: discord.Member, newnick: str = None):
		if newnick is None:
			await member.edit(nick=None)
			await ctx.send(f'Нікнейм скинуто для користувача **{member.display_name}**')
		else:
			await member.edit(nick=newnick)
			await ctx.send(f'Нік **{newnick}** для користувача **{member.display_name}** встановлено')


	@commands.hybrid_command(
		name="vacban",
		description="Банить користувача."
	)
	@commands.has_permissions(administrator=True)
	async def vacban(self, ctx, member: discord.Member, reason: str = None):
		await member.ban(reason=reason)
		await ctx.send(
			f'Користувач **{member.display_name}** був заблокований за причини **{reason}** користувачем {ctx.author.display_name}')


	@commands.hybrid_command(
		name="mute",
		description="Мутить користувача у войсі."
	)
	@commands.has_permissions(administrator=True)
	async def mute(self, ctx, member: discord.Member):
		await member.edit(mute=True)
		await ctx.send(f'Користувач **{member.display_name}** замучений у войсі')


	@commands.hybrid_command(
		name="unmute",
		description="Розмучує користувача у войсі."
	)
	@commands.has_permissions(administrator=True)
	async def unmute(self, ctx, member: discord.Member):
		await member.edit(mute=False)
		await ctx.send(f'Користувач **{member.display_name}** розмучений у войсі')


	@commands.hybrid_command(
		name="deafen",
		description="Глушить користувача у войсі."
	)
	@commands.has_permissions(administrator=True)
	async def deafen(self, ctx, member: discord.Member):
		await member.edit(deafen=True)
		await ctx.send(f'Користувач **{member.display_name}** заглушений у войсі')

	@commands.hybrid_command(
		name="undeafen",
		description="Розлушує користувача у войсі."
	)
	@commands.has_permissions(administrator=True)
	async def undeafen(self, ctx, member: discord.Member):
		await member.edit(deafen=False)
		await ctx.send(f'Користувач **{member.display_name}** розглушений у войсі')


	@commands.hybrid_command(
		name="poll",
		description="Створює голосування."
	)
	async def poll(self, ctx, action: str, time: int, member: discord.Member = None, *, reason: str = "По фану"):
		if not member:
			member = ctx.author

		message = await ctx.send(f'Запущено голосування\nУчасник: {member}\nДія: {action}\nПричина: {reason}')
		await message.add_reaction("👍🏻")
		await message.add_reaction("👎🏾")

		await asyncio.sleep(time)

		message = await ctx.channel.fetch_message(message.id)
		upvote = next((react for react in message.reactions if str(react.emoji) == "👍🏻"), None)
		downvote = next((react for react in message.reactions if str(react.emoji) == "👎🏾"), None)

		upvote_count = upvote.count - 1 if upvote else 0
		downvote_count = downvote.count - 1 if downvote else 0

		await ctx.send(f'Голосування завершено!\n👍🏻 За: {upvote_count}\n👎🏾 Проти: {downvote_count}')

		"""
		TODO: написать логіку команди
		створить словник action's, де кожна дія буде дорівнювати def name_action
		"""

async def setup(bot):
	await bot.add_cog(Moderation(bot))
