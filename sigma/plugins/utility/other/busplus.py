import os
import discord
import aiohttp
from io import BytesIO
from PIL import Image


async def busplus(cmd, message, args):
    if args:
        if len(args) == 2:
            line_number = args[0]
            terminus = args[1]
            if terminus == '1' or terminus == '2':
                image_url = f'https://www.busevi.com/red-voznje/gradski-prevoz-beograd/{line_number}-{terminus}.png'
                image_location = f'cache/bus_{message.id}.png'
                async with aiohttp.ClientSession() as session:
                    async with session.get(image_url) as data:
                        image_data = await data.read()
                        image = BytesIO(image_data)
                with Image.open(image) as image_bytes:
                    image_bytes.save(image_location)
                    await message.channel.send(file=discord.File(image_location, filename=f'bus_{line_number}.png'))
                    os.remove(image_location)
                    response = None
            else:
                response = discord.Embed(color=0xDB0000, title='❗ Invalid terminus number. 1 and 2 are accepted.')
        else:
            response = discord.Embed(color=0xDB0000, title='❗ Invalid number of arguments.')
    else:
        response = discord.Embed(color=0xDB0000, title='❗ No arguments passed.')
    if response:
        await message.channel.send(embed=response)
