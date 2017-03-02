import discord
import asyncio
from sigma.core.utils import user_avatar
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
    srv_queue = cmd.music.get_queue(message.server.id)
    voice_connected = cmd.bot.is_voice_connected(message.server)
    if not voice_connected:
        await cmd.bot.join_voice_channel(message.author.voice_channel)
        embed = discord.Embed(title=':white_check_mark: Joined ' + message.author.voice_channel.name, color=0x66cc66)
        await cmd.bot.send_message(message.channel, None, embed=embed)
    if len(srv_queue.queue) == 0:
        embed = discord.Embed(
            title=':warning: The queue is empty', color=0xFF9900)
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    player = cmd.music.get_player(message.server.id)
    if player:
        if player.is_playing():
            embed = discord.Embed(
                title=':warning: Already playing in ' + cmd.bot.voice_client_in(message.server).channel.name,
                color=0xFF9900)
            await cmd.bot.send_message(message.channel, None, embed=embed)
            return
    voice_instance = cmd.bot.voice_client_in(message.server)
    while cmd.music.get_queue(message.server.id) and len(cmd.music.get_queue(message.server.id).queue) != 0:
        item = cmd.music.get_from_queue(message.server.id)
        video = item['video']
        item_url = item['url']
        await cmd.music.make_yt_player(message.server.id, voice_instance, item_url)
        player = cmd.music.get_player(message.server.id)
        if not player:
            print('No player.')
            return
        def_vol = cmd.music.get_volume(cmd.db, message.server.id)
        if def_vol:
            player.volume = def_vol / 100
        player.start()
        cmd.db.add_stats('MusicCount')
        embed = discord.Embed(color=0x0099FF)
        embed.add_field(name='🎵 Now Playing', value=video.title)
        embed.set_thumbnail(url=video.thumb)
        embed.set_author(name=f'{message.author.name}#{message.author.discriminator}',
                         icon_url=user_avatar(item['requester']))
        embed.set_footer(text=f'Duration: {video.duration}')
        await cmd.bot.send_message(message.channel, None, embed=embed)
        while not player.is_done():
            await asyncio.sleep(2)
        cmd.music.kill_player(message.server.id)
    await voice_instance.disconnect()
    embed = discord.Embed(title=':white_check_mark: Queue Depleted', color=0x66cc66)
    await cmd.bot.send_message(message.channel, None, embed=embed)
