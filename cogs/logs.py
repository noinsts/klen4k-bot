import discord
from discord.ext import commands

import config as cfg


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        log_channel = member.guild.get_channel(cfg.LOG_CHANNEL_ID)

        if not log_channel:
            print('Log channel is not found')

        if before.channel != after.channel:
            if before.channel is None:
                action = "зайшов у "
                channel_name = after.channel.name
            elif after.channel is None:
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

        await log_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Logs(bot))
