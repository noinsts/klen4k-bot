import random

import discord
from discord.ext import commands

from src import config as cfg


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_command(
        name = 'afk',
        description = 'Відправляє випадкового користувача з вашого войсу в афк войс'
    )
    async def afk(self, ctx, member: discord.Member):
        guild = self.bot.get_guild(cfg.GUILD_ID)
        afk = guild.get_channel(cfg.AFK_ID)
        voice = member.voice

        if voice is None:
            await ctx.send("Помилка, цієї людини немає в войсі")
        else:
            await member.move_to(afk)
            await ctx.send(f"**{member.display_name}** відправлений до **{afk.name}**")


    @commands.hybrid_command(
        name = 'roulette',
        description = 'Кікає випадкову людину з вашого войсу'
    )
    async def roulette(self, ctx):
        voice = ctx.author.voice
        channel = voice.channel
        members = channel.members
        members_names = [member for member in members]

        kick = random.choice(members_names)

        if voice is None:
            await ctx.send("Щоб використовувати цю команду потрібно бути в войсі")
        else:
            await kick.move_to(None)
            await ctx.send(f"З войса **{channel.name}** було кікнуто **{kick.display_name}**, тому що так нада")


    @commands.hybrid_command(
        name = 'private',
        description = 'Відправляє вас та вашого друга в окремий войс'
    )
    async def private(self, ctx, member: discord.Member):
        duo = ctx.guild.get_channel(cfg.DUO_ID)
        lenovo = ctx.guild.get_channel(cfg.LENOVO_ID)

        members_duo = duo.members
        members_lenovo = lenovo.members

        if len(members_duo) == 0:
            await ctx.author.move_to(duo)
            await member.move_to(duo)
            await ctx.send(f'**{ctx.author}** та **{member}** відправленні до **{duo.name}**')
        elif len(members_lenovo) == 0:
            await ctx.author.move_to(lenovo)
            await member.move_to(lenovo)
            await ctx.send(f'**{ctx.author}** та **{member}** відправленні до **{lenovo.name}**')
        else:
            await ctx.send('Вільного канала не знайдено.')


    @commands.hybrid_command(
        name = 'vlock',
        description = 'Блокує ваш войс'
    )
    async def vlock(self, ctx):
        voice = ctx.author.voice

        if voice is None:
            await ctx.send('Щоб використовувати цю команду потрібно знаходитись у войсі')
            return

        channel = voice.channel

        overwrites = channel.overwrites_for(ctx.guild.default_role)
        overwrites.connect = False

        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
        await ctx.send(f'Доступ до канала **{channel.name}** простим смертним заблоковано')


    @commands.hybrid_command(
        name = 'vunlock',
        description = 'Розблоковує ваш войс'
    )
    async def vunlock(self, ctx):
        voice = ctx.author.voice

        if voice is None:
            await ctx.send('Щоб використовувати цю команду потрібно знаходитись у войсі')
            return

        channel = voice.channel

        overwrites = channel.overwrites_for(ctx.guild.default_role)
        overwrites.connect = True

        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
        await ctx.send(f'Доступ до канала **{channel.name}** простим смертним дозволено')


async def setup(bot):
    await bot.add_cog(Voice(bot))
