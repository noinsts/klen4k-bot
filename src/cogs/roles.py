import os
import json

import discord
from discord.ext import commands

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')


class Config:
    def __init__(self, config_path=CONFIG_PATH):
        with open(config_path, 'r') as f:
            self._config = json.load(f)

    def __getattr__(self, name):
        return self._config.get(name)
    
cfg = Config()


class Roles(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


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
