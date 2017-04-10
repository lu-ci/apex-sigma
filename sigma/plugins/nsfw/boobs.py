import random
import discord
import aiohttp


async def boobs(cmd, message, args):
    api_base = 'http://api.oboobs.ru/boobs/'
    number = random.randint(1, 10303)
    url_api = api_base + str(number)
    async with aiohttp.ClientSession() as session:
        async with session.get(url_api) as data:
            data = await data.json()
            data = data[0]
    image_url = 'http://media.oboobs.ru/' + data['preview']
    embed = discord.Embed(color=0x9933FF)
    embed.set_image(url=image_url)
    await message.channel.send(None, embed=embed)
