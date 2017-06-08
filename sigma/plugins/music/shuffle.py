import discord
import random
import asyncio


async def shuffle(cmd, message, args):
    queue = cmd.music.get_queue(message.guild.id)
    queue_new = asyncio.Queue()
    if queue:
        if not queue.empty():
            q_list = []
            while not cmd.music.get_queue(message.guild.id).empty():
                q_item = await cmd.music.get_queue(message.guild.id).get()
                q_list.append(q_item)
            random.shuffle(q_list)
            for item in q_list:
                await queue_new.put(item)
            cmd.music.queues.update({message.guild.id: queue_new})
            embed = discord.Embed(color=0x0099FF, title='🔀 Queue Shuffled')
            await message.channel.send(None, embed=embed)
