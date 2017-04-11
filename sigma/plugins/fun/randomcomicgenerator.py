import discord
import aiohttp
from lxml import html as l


async def randomcomicgenerator(cmd, message, args):
    comic_url = 'http://explosm.net/rcg/'
    async with aiohttp.ClientSession(cookies={'explosm': 'nui4hbhpq55tr4ouqknb060jr4'}) as session:
        async with session.get(comic_url) as data:
            page = await data.text()
    root = l.fromstring(page)
    comic_element = root.cssselect('#rcg-comic')
    comic_img_url = comic_element[0][0].attrib['src']
    if comic_img_url.startswith('//'):
        comic_img_url = 'https:' + comic_img_url
    embed = discord.Embed(color=0x1ABC9C)
    embed.set_image(url=comic_img_url)
    await message.channel.send(None, embed=embed)
