import discord
from discord.ext import commands

from src.cogs.base import BaseCog

class Roles(BaseCog):
	def __init__(self, bot):
		super().__init__(bot)


	@commands.hybrid_command(
		name = 'role',
		description = 'Додає/забирає x роль учаснику'
	)
	@commands.has_permissions(administrator=True)
	async def role(self, ctx, action: str, role: str, member: discord.Member = None):
		member = member or ctx.author

		roles = {
			"elite": cfg.ELITE_ROLE_ID,
			"rust": cfg.RUST_ROLE_ID
		}

		role_id = roles.get(role.lower())
		role = ctx.guild.get_role(role_id)

		if action.lower() == "add":
			await member.add_roles(role)
			await ctx.send(f"Користувачу **{member.name}** надана роль **{role.name}**")
		elif action.lower() == "remove":
			await member.remove_roles(role)
			await ctx.send(f"У користувача **{member.name}** роль **{role.name}** забрано")
		else:
			await ctx.send("Вибачте спробуйте так: .role add/remove elite/rust @name")


async def setup(bot):
	await bot.add_cog(Roles(bot))
