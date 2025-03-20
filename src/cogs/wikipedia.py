import  wikipediaapi

import discord
from discord.ext import commands


class Wikipedia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.wiki = wikipediaapi.Wikipedia(user_agent="klen4k-bot (contact: @noinsts (github))", language="uk")

    @commands.command(aliases=['wiki'])
    async def search(self, ctx, *, query: str):
        page = self.wiki.page(query)

        if not page.exists():
            await ctx.send(f'Сторінку **{query}** не знайдено')
            return

        embed = discord.Embed(title=page.title, color=0xFFFFFF)

        summary = page.summary

        if len(summary) > 1000:
            summary = summary[:1000] + "..."

        embed.add_field(name='Опис', value=summary, inline=False)

        url = page.fullurl
        embed.set_footer(text=f'🔗 {url}')

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Wikipedia(bot))
