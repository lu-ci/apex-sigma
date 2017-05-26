import random
import aiohttp
import discord
from lxml import html


async def grab_post_list(tags):
    links = []
    for x in range(0, 20):
        resource = f'http://safebooru.org/index.php?page=dapi&s=post&q=index&tags={tags}&pid={x}'
        async with aiohttp.ClientSession() as session:
            async with session.get(resource) as data:
                data = await data.read()
        posts = html.fromstring(data)
        for post in posts:
            if 'file_url' in post.attrib:
                file_url = post.attrib['file_url']
                extention = file_url.split('.')[-1]
                if extention in ['png', 'jpg', 'jpeg', 'gif']:
                    height = int(post.attrib['height'])
                    width = int(post.attrib['width'])
                    if width < 2000 and height < 2000:
                        links.append(post)
    return links


def generate_embed(post, titles, color=0xff6699):
    image_url = post.attrib['file_url']
    image_source = f'http://safebooru.org/index.php?page=post&s=view&id={post.attrib["id"]}'
    if image_url.startswith('//'):
        image_url = 'https:' + image_url
    embed = discord.Embed(color=color)
    icon_url = 'http://3.bp.blogspot.com/_SUox58HNUCI/SxtiKLuB7VI/AAAAAAAAA08/s_st-jZnavI/s400/Azunyan+fish.jpg'
    embed.set_author(name=random.choice(titles), icon_url=icon_url, url=image_source)
    embed.set_image(url=image_url)
    return embed
