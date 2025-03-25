import asyncio
import discord
from discord.ext import commands
from datetime import timedelta
from src.logger import setup_logger


class Moderation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.log = setup_logger()

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

		if time < 30:
			await ctx.send('Мінімальний час голосування 30 секунд')
			return

		actions = {
			"voice_kick": lambda member, reason: member.move_to(None, reason=reason),
			"kick": lambda member, reason: member.kick(reason=reason),
			"ban": lambda member, reason: member.ban(reason=reason),
			"timeout": lambda member, reason: member.timeout(duration=60, reason=reason)
		}

		messages = {
			"voice_kick": {
				"success": "✅ {member} був викинутий з голосового каналу!",
				"fail": "❌ Не вдалося викинути {member} з голосового!"
			},
			"kick": {
				"success": "✅ {member} був кікнутий із серверу!",
				"fail": "❌ Не вдалося кікнути {member}!",
				"not_enough_votes": "⚠️ Замало голосів, щоб кікнути {member}!"
			},
			"ban": {
				"success": "✅ {member} отримав бан!",
				"fail": "❌ Не вдалося забанити {member}!",
				"not_enough_votes": "⚠️ Замало голосів, щоб забанити {member}!"
			},
			"timeout": {
				"success": "✅ {member} отримав таймаут на 60 секунд!",
				"fail": "❌ Не вдалося видати таймаут {member}!"
			},
			"no_action": "ℹ️ Голоси не набрані – {member} залишається на сервері. Пощастило цього разу! 😉"
		}

		action_in_embed = {
			"ban" : "Блокування користувача на поточному сервері",
			"kick" : "Кік користувача з серверу",
			"timeout" : "Тимчасовий блок користувача",
			"voice_kick" : "Викидання користувача з поточного голосового каналу"
		}

		if action not in actions:
			await ctx.send('Помилка action не знайдено, спробуйте voice_kick, kick, ban, timeout')
			return


		embed = discord.Embed(title='Розпочато голосування', color = discord.Color.blue())

		embed.add_field(name='Учасник', value=member.display_name, inline=False)
		embed.add_field(name='Дія', value=action_in_embed[action], inline=False)
		embed.add_field(name='Причина', value=reason, inline=False)
		embed.add_field(name='Час до закінчення голосування', value=f'{time} секунд', inline=False)

		embed.set_footer(text=f'Розпочав голосування: {ctx.author.display_name}')

		message = await ctx.send(embed=embed)

		await message.add_reaction("👍🏻")
		await message.add_reaction("👎🏾")

		await asyncio.sleep(time)

		message = await ctx.channel.fetch_message(message.id)
		upvote = next((react for react in message.reactions if str(react.emoji) == "👍🏻"), None)
		downvote = next((react for react in message.reactions if str(react.emoji) == "👎🏾"), None)

		upvote_count = upvote.count - 1 if upvote else 0
		downvote_count = downvote.count - 1 if downvote else 0

		stats = discord.Embed(title='Результати голосування', color=discord.Color.blue())

		stats.add_field(name='👍🏻 За:', value=upvote_count, inline=False)
		stats.add_field(name='👎🏾 Проти:', value=downvote_count, inline=False)

		if upvote_count > downvote_count:
			if (action == 'ban' or action == 'kick') and upvote_count < 3:
				result = messages[action]["not_enough_votes"].format(member=member.mention)
			else:
				try:
					await actions[action](member, reason)
					result = messages[action]["success"].format(member=member.mention)
				except Exception as e:
					result = messages[action]["fail"].format(member=member.mention)
					self.log.info(f"Помилка під час виконання {action}: {e}")
		else:
			result = messages["no_action"].format(member=member.mention)

		stats.add_field(name='Результат', value=result, inline=False)

		await ctx.send(embed=stats)


async def setup(bot):
	await bot.add_cog(Moderation(bot))
