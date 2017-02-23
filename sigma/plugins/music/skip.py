import discord
from .music_controller import get_player, get_queue, del_from_queue

async def skip(cmd, message, args):
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
    if len(get_queue(message.server)) == 1:
        embed = discord.Embed(
            title=':warning: This is the last song in the queue', color=0xFF9900)
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    embed = discord.Embed(title=':white_check_mark: Skip Acknowledged', color=0x66CC66)
    embed.set_footer(text='Skipping ' + player.title)
    await cmd.bot.send_message(message.channel, None, embed=embed)
    player.stop()
