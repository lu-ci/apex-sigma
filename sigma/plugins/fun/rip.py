import discord
import aiohttp
import os
from PIL import Image
from io import BytesIO
from sigma.core.utils import user_avatar


async def rip(cmd, message, args):
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    avatar_url = user_avatar(target) + '?size=128'
    async with aiohttp.ClientSession() as session:
        async with session.get(avatar_url) as data:
            avatar = await data.read()
            avatar = BytesIO(avatar)
    base = Image.open(cmd.resource('img/base.png'))
    tomb = Image.open(cmd.resource('img/tombstone.png'))
    avatar_img = Image.open(avatar)
    avatar_img = avatar_img.resize((108, 108), Image.ANTIALIAS)
    base.paste(avatar_img, (60, 164))
    base.paste(tomb, (0, 0), tomb)
    base.save(f'cache/rip_{message.id}.png')
    await message.channel.send(file=discord.File(f'cache/rip_{message.id}.png'))
    os.remove(f'cache/rip_{message.id}.png')
