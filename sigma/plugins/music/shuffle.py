import discord
import random


async def shuffle(cmd, message, args):
    queue = cmd.music.get_queue(message.guild.id)
    if queue:
        random.shuffle(cmd.music.get_queue(message.guild.id).queue)
        embed = discord.Embed(color=0x0099FF, title='🔀 Queue Shuffled')
        await message.channel.send(None, embed=embed)
