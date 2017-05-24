import aiohttp
import random
import discord
from lxml import html


links = []

async def nyaa(cmd, message, args):
    resource = 'http://safebooru.org/index.php?page=dapi&s=post&q=index&tags=nekomimi+female+solo'
    if not links:
        async with aiohttp.ClientSession() as session:
            async with session.get(resource) as data:
                data = await data.read()
        posts = html.fromstring(data)
        for post in posts:
            file_url = post.attrib['file_url']
            extention = file_url.split('.')[-1]
            if extention in ['png', 'jpg', 'jpeg', 'gif']:
                links.append(file_url)
    random.shuffle(links)
    image_url = links.pop()
    if image_url.startswith('//'):
        image_url = 'http:' + image_url
    embed = discord.Embed(color=0xff6699)
    embed.set_image(url=image_url)
    await message.channel.send(None, embed=embed)
