import discord
import random
from .music_controller import add_to_queue


async def autoplaylist(cmd, message, args):
    if not message.author.voice_channel:
        embed = discord.Embed(
            title=':warning: I don\'t see you in a voice channel', color=0xFF9900)
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    lines = (line.rstrip('\n') for line in open(cmd.resource('autoplaylist.txt')))
    line_list = []
    for line in lines:
        line_list.append(line)
    random.shuffle(line_list)
    for line in line_list:
        add_to_queue(message.server, message.author.name, 'YouTube', line, 'Autoplaylist Item')
    embed = discord.Embed(color=0x66CC66, title=':white_check_mark: Autoplaylist Added To Queue')
    await cmd.bot.send_message(message.channel, None, embed=embed)
