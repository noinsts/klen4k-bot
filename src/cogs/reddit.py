import praw
import os
from dotenv import load_dotenv
import random
import discord
from discord.ext import commands

load_dotenv()


class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(
            client_id = os.getenv("CLIENT_REDDIT_API"),
            client_secret = os.getenv("SECRET_REDDIT_API"),
            user_agent="klen4k-bot (by u/Alarming_State8450)"
        )

    @commands.command()
    async def top(self, ctx, subreddit_name: str = "python"):
        subreddit = self.reddit.subreddit(subreddit_name)
        post = next(subreddit.hot(limit=1))

        embed = discord.Embed(
            title=f'Топ пост з r/{subreddit.title}',
            description=post.selftext[:1000] + "...",
            color=discord.Color.orange()
        )

        embed.set_footer(text=f'👍🏻 {post.score}, 💬 {post.num_comments} коментарів')

        await ctx.send(embed=embed)

    @commands.command()
    async def meme(self, ctx):
        try:
            subreddit = self.reddit.subreddit("ukr_memes")
            posts = list(subreddit.hot(limit=50))
            post = random.choice(posts)

            embed = discord.Embed(
                title=f'Пост з r/{subreddit.title}',
                url=post.url,
                color=discord.Color.orange()
            )

            embed.set_image(url=post.url)
            embed.set_footer(text=f'👍🏻 {post.score}, 💬 {post.num_comments} коментарів')

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Помилка: `{e}`")



async def setup(bot):
    await bot.add_cog(Reddit(bot))
