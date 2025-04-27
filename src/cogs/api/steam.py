import os

import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv

from ..base import BaseCog

load_dotenv()


class Steam(BaseCog):
	def __init__(self, bot):
		super().__init__(bot)


	@staticmethod
	def get_steam_id(username):
		url = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={os.getenv("API_KEY")}&vanityurl={username}"
		response = requests.get(url).json()
		return response["response"].get("steamid")


	@staticmethod
	def get_player_info(steam_id):
		url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={os.getenv("API_KEY")}&steamids={steam_id}"
		response = requests.get(url).json()
		players = response["response"]["players"]
		return players[0] if players else None


	@commands.command()
	async def steaminfo(self, ctx, username: str):
		steam_id = self.get_steam_id(username)
		player_info = self.get_player_info(steam_id)

		if not steam_id:
			await ctx.send("Не вдалося знайти Steam ID.")
			return

		if not player_info:
			await ctx.send("Про користувача немає інформації")

		embed = discord.Embed(title=player_info["personaname"], url = player_info["profileurl"], color = discord.Color.red())

		embed.set_thumbnail(url=player_info["avatarfull"])
		embed.add_field(name='Статус', value = 'Онлайн' if player_info["personastate"] == 1 else "Офлайн", inline = False)

		await ctx.send(embed=embed)


async def setup(bot):
	await bot.add_cog(Steam(bot))
