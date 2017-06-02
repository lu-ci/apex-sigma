import arrow
import discord
from sigma.core.utils import user_avatar
from .common import get_time_difference


async def move_log_leave(ev, member):
    try:
        log_channel_id = ev.db.get_settings(member.guild.id, 'LoggingChannel')
    except:
        log_channel_id = None
    if log_channel_id:
        log_channel = discord.utils.find(lambda x: x.id == log_channel_id, member.guild.channels)
        if log_channel:
            response = discord.Embed(color=0xDB0000, timestamp=arrow.utcnow().datetime)
            response.set_author(name=f'A Member Has Left', icon_url=user_avatar(member))
            response.add_field(name='📤 Leaving Member', value=f'{member.mention}\n{member.name}#{member.discriminator}')
            new_acc, diff_msg = get_time_difference(member, leave=True)
            response.add_field(name='🕑 Member Joined', value=f'{diff_msg.title()}', inline=True)
            response.set_footer(text=f'UserID: {member.id}')
            await log_channel.send(embed=response)
        else:
            ev.db.set_settings(member.guild.id, 'LoggingChannel', None)
