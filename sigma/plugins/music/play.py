import discord
import asyncio
import datetime
from .music_controller import get_player, get_queue, del_from_queue, make_yt_player


async def play(cmd, message, args):
    if not message.author.voice_channel:
        embed = discord.Embed(
            title=':warning: I don\'t see you in a voice channel', color=0xFF9900)
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    srv_queue = get_queue(message.server)
    voice_connected = cmd.bot.is_voice_connected(message.server)
    if not voice_connected:
        embed = discord.Embed(title=':warning: I am not in a voice channel currently', color=0xFF9900)
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    if len(srv_queue) == 0:
        embed = discord.Embed(
            title=':warning: The queue is empty', color=0xFF9900)
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    while len(srv_queue) != 0:
        item_info = srv_queue[0]
        item_type = item_info['Type']
        item_req = item_info['Requester']
        item_url = item_info['Location']
        voice_instance = cmd.bot.voice_client_in(message.server)
        await make_yt_player(message.server, voice_instance, item_url)
        player = get_player(message.server)
        player.play()
        embed = discord.Embed(title='ℹ Now Playing From ' + item_type)
        embed.add_field(name='Title', value=player.title)
        embed.set_footer(
            text='Requested by ' + item_req + '. Duration: ' + str(datetime.timedelta(seconds=player.duration)))
        while not player.is_done():
            await asyncio.sleep(3)
        del_from_queue(message.server, 0)
