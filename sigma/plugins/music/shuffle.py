import discord
import random


async def shuffle(cmd, message, args):
    queue = cmd.music.get_queue(message.server.id)
    if queue:
        random.shuffle(cmd.music.get_queue(message.server.id).queue)
        embed = discord.Embed(color=0x66CC66, title=':white_check_mark: Queue Shuffled')
        await cmd.bot.send_message(message.channel, None, embed=embed)
