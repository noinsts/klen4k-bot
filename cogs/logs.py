import discord
from discord.ext import commands

import config as cfg

from database import Database


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    """Запит дозволу відображати логи"""


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_log_visibility(self, ctx, action: str, allow: bool):
        if not action:
            await ctx.send('Введіть дію')
            return

        if not allow:
            await ctx.send('Введіть значення')
            return

        self.db.set_log_visibility(action, allow)

        await ctx.send(f'Успіх! **{action}** встановлено значення **{allow}**')


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def is_log_allowed(self, ctx, action: str):
        if not action:
            await ctx.send('Помилка, введіть дію')
            return

        await ctx.send(f'**{self.db.is_log_allowed(action)}**')


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def delete_log_action(self, ctx, action: str):
        if not action:
            await ctx.send('Помилка, введіть дію')
            return

        self.db.delete_log_action(action)
        await ctx.send(f'Успіх! {action} видалено')


    """Логування"""


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        log_channel = member.guild.get_channel(cfg.LOG_CHANNEL_ID)

        if not log_channel:
            print('Log channel is not found')

        if before.channel != after.channel:
            if not before.channel:
                action = "зайшов у "
                channel_name = after.channel.name
            elif not after.channel:
                action = "вийшов з "
                channel_name = before.channel.name
            else:
                action = "перемістився в "
                channel_name = after.channel.name
        else:
            return


        embed = discord.Embed(title='Новий лог',
                              description=f'**{member.display_name}** {action} **{channel_name}**',
                              color = discord.Color.red()
        )

        if self.db.is_log_allowed("voice_logs"):
            await log_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Logs(bot))
