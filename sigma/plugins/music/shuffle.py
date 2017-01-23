import discord
import random
from .music_controller import get_queue, purge_queue, add_to_queue


async def shuffle(cmd, message, args):
    queue = get_queue(message.server)
    if not queue or len(queue) == 0:
        embed = discord.Embed(title=':warning: The Queue Is Empty', color=0xFF9900)
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    first_item = queue[0]
    rest_of_queue = queue[1:]
    random.shuffle(rest_of_queue)
    purge_queue(message.server)
    add_to_queue(message.server, first_item['Requester'], first_item['Type'], first_item['Location'],
                 first_item['Title'])
    for item in rest_of_queue:
        add_to_queue(message.server, item['Requester'], item['Type'], item['Location'],
                     item['Title'])
    embed = discord.Embed(title=':white_check_mark: The Queue Has Been Shuffled', color=0x66CC66)
    await cmd.bot.send_message(message.channel, None, embed=embed)
