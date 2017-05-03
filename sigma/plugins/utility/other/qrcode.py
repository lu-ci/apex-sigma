import discord
import aiohttp
from config import MashapeKey
from io import BytesIO


async def qrcode(cmd, message, args):
    if args:
        url = 'https://neutrinoapi-qr-code.p.mashape.com/qr-code'
        content = ' '.join(args)
        headers = {
            "X-Mashape-Key": MashapeKey,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        params = {
            "bg-color": "#FFFFFF",
            "content": content,
            "fg-color": "#000000",
            "height": 512,
            "width": 512
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=params, headers=headers) as data:
                data = await data.read()
        output = discord.File(BytesIO(data), filename=f'qr_{message.id}.png')
        await message.channel.send(file=output)
        if args[-1].startswith('del'):
            try:
                await message.delete()
            except:
                pass
