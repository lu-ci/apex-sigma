import discord
import aiohttp
import os
from PIL import Image
from io import BytesIO


async def rip(cmd, message, args):
    result = ''
    mentioned_avatar = ''

    if not message.mentions:
        await message.channel.send(cmd.help())
        return

    for user in message.mentions:
        result = result + 'The Avatar of ' + user.display_name + " is " + user.avatar_url
        mentioned_avatar = user.avatar_url
        if mentioned_avatar == '':
            mentioned_avatar = user.default_avatar_url
    async with aiohttp.ClientSession() as session:
        async with session.get(mentioned_avatar) as data:
            user_avatar = await data.read()
            user_avatar = BytesIO(user_avatar)
    base = Image.open(cmd.resource('img/base.png'))
    tomb = Image.open(cmd.resource('img/tombstone.png'))
    avatar_img = Image.open(user_avatar)
    avatar_img = avatar_img.resize((108, 108), Image.ANTIALIAS)
    base.paste(avatar_img, (60, 164))
    base.paste(tomb, (0, 0), tomb)
    base.save(f'cache/rip_{message.id}.png')
    await message.channel.send(file=discord.File(f'cache/rip_{message.id}.png'))
    os.remove(f'cache/rip_{message.id}.png')
