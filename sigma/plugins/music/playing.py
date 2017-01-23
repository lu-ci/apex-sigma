import discord
import datetime
from .music_controller import get_player, get_queue


async def playing(cmd, message, args):
    player = get_player(message.server)
    if not player:
        embed = discord.Embed(title=':warning: No Player Instance Found', color=0xFF9900)
    else:
        if not player.is_playing():
            embed = discord.Embed(title=':warning: The Player Is Not Active', color=0xFF9900)
        else:
            queue = get_queue(message.server)
            item_info = queue[0]
            item_type = item_info['Type']
            item_req = item_info['Requester']
            embed = discord.Embed(title='ℹ Now Playing From ' + item_type, color=0x0099FF)
            embed.add_field(name='Title', value=player.title)
            embed.set_footer(
                text='Requested by ' + item_req + '. Duration: ' + str(datetime.timedelta(seconds=player.duration)))
    await cmd.bot.send_message(message.channel, None, embed=embed)

