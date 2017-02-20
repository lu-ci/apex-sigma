import discord
import asyncio
import datetime
from .music_controller import get_player, get_queue, del_from_queue, make_yt_player, del_player, get_volume, purge_queue
from config import Prefix


async def play(cmd, message, args):
    if args:
        embed = discord.Embed(color=0xDB0000, title=':exclamation: Use ' + Prefix + 'queue to add stuff.')
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    if not message.author.voice_channel:
        embed = discord.Embed(
            title=':warning: I don\'t see you in a voice channel', color=0xFF9900)
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    srv_queue = get_queue(message.server)
    voice_connected = cmd.bot.is_voice_connected(message.server)
    if not voice_connected:
        await cmd.bot.join_voice_channel(message.author.voice_channel)
        embed = discord.Embed(title=':white_check_mark: Joined ' + message.author.voice_channel.name, color=0x66cc66)
        await cmd.bot.send_message(message.channel, None, embed=embed)
    if len(srv_queue) == 0:
        embed = discord.Embed(
            title=':warning: The queue is empty', color=0xFF9900)
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    player = get_player(message.server)
    if player:
        if player.is_playing():
            embed = discord.Embed(
                title=':warning: Already playing in ' + cmd.bot.voice_client_in(message.server).channel.name,
                color=0xFF9900)
            await cmd.bot.send_message(message.channel, None, embed=embed)
            return
    voice_instance = cmd.bot.voice_client_in(message.server)
    while get_queue(message.server) and len(get_queue(message.server)) != 0:
        item_info = srv_queue[0]
        item_type = item_info['Type']
        item_req = item_info['Requester']
        item_url = item_info['Location']
        await make_yt_player(message.server, voice_instance, item_url)
        player = get_player(message.server)
        if not player:
            return
        def_vol = get_volume(message.server)
        if def_vol:
            player.volume = def_vol
        player.start()
        cmd.db.add_stats('MusicCount')
        embed = discord.Embed(title='ℹ Now Playing From ' + item_type, color=0x0099FF)
        embed.add_field(name='Title', value=player.title)
        embed.set_footer(
            text='Requested by ' + item_req + '. Duration: ' + str(datetime.timedelta(seconds=player.duration)))
        await cmd.bot.send_message(message.channel, None, embed=embed)
        while not player.is_done():
            await asyncio.sleep(2)
        player.stop()
        del_player(message.server)
        del_from_queue(message.server, 0)
    purge_queue(message.server)
    await voice_instance.disconnect()
