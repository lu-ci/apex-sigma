import aiohttp
from PIL import Image
from io import BytesIO
import os


async def dog(cmd, message, args):
    doggie_url = 'http://www.randomdoggiegenerator.com/randomdoggie.php'
    async with aiohttp.ClientSession() as session:
        async with session.get(doggie_url) as data:
            doggie_image = await data.read()
    with Image.open(BytesIO(doggie_image)) as img:
        img.save(f'cache/pupper_{message.id}.png')
    await message.channel.send_file(f'cache/pupper_{message.id}.png')
    os.remove(f'cache/pupper_{message.id}.png')
