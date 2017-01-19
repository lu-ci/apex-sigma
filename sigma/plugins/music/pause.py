import discord
from .music_controller import get_player, get_queue, del_from_queue, make_yt_player, del_player, get_volume


async def pause(cmd, message, args):
    if not message.author.voice_channel:
        embed = discord.Embed(
            title=':warning: I don\'t see you in a voice channel', color=0xFF9900)
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    player = get_player(message.server)
    if not player:
        embed = discord.Embed(
            title=':warning: No player instance currently exists', color=0xFF9900)
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    if not player.is_playing():
        embed = discord.Embed(
            title=':warning: The player is not currently playing', color=0xFF9900)
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    player.pause()
