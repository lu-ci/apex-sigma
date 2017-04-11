import aiohttp
import random
import discord
from lxml import html


async def safebooru(cmd, message, args):
    if not args:
        tag = 'cute'
    else:
        tag = ' '.join(args)
        tag = tag.replace(' ', '+')
    resource = 'http://safebooru.org/index.php?page=dapi&s=post&q=index&tags=' + tag
    async with aiohttp.ClientSession() as session:
        async with session.get(resource) as data:
            data = await data.text()
    posts = html.fromstring(data)
    choice = random.choice(posts)
    image_url = choice.attrib['file_url']
    if image_url.startswith('//'):
        image_url = 'http:' + image_url
    embed = discord.Embed(color=0xff6699)
    embed.set_image(url=image_url)
    await message.channel.send(None, embed=embed)
