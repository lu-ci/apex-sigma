import discord
import random
import aiohttp
from lxml import html as l


async def cyanideandhappiness(cmd, message, args):
    comic_number = random.randint(1, 4562)
    comic_url = f'http://explosm.net/comics/{comic_number}/'
    async with aiohttp.ClientSession() as session:
        async with session.get(comic_url) as data:
            page = await data.text()
    root = l.fromstring(page)
    comic_element = root.cssselect('#main-comic')
    comic_img_url = comic_element[0].attrib['src']
    if comic_img_url.startswith('//'):
        comic_img_url = 'https:' + comic_img_url
    embed = discord.Embed(color=0x1ABC9C)
    embed.set_image(url=comic_img_url)
    await message.channel.send(None, embed=embed)
