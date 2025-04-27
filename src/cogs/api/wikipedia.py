import wikipediaapi

import discord
from discord.ext import commands

from ..base import BaseCog


class Wikipedia(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.wiki = wikipediaapi.Wikipedia(user_agent="klen4k-bot (contact: @noinsts (github))", language="uk")


    @commands.hybrid_command(
        name = 'search',
        description = 'Шукає інформацію в вікі',
        aliases=['wiki']
    )
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
