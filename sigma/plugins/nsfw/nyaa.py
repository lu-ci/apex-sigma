import aiohttp
import random
import discord
from lxml import html

links = []


async def fill_links():
    for x in range(0, 20):
        resource = f'http://safebooru.org/index.php?page=dapi&s=post&q=index&tags=cat_ears&pid={x}'
        async with aiohttp.ClientSession() as session:
            async with session.get(resource) as data:
                data = await data.read()
        posts = html.fromstring(data)
        for post in posts:
            if 'file_url' in post.attrib:
                file_url = post.attrib['file_url']
                extention = file_url.split('.')[-1]
                if extention in ['png', 'jpg', 'jpeg', 'gif']:
                    links.append(file_url)


async def nyaa(cmd, message, args):
    if not links:
        filler_message = discord.Embed(color=0xff6699, title='🐱 One moment, filling Sigma with catgirls...')
        fill_notify = await message.channel.send(embed=filler_message)
        await fill_links()
        filler_done = discord.Embed(color=0xff6699, title=f'🐱 We added {len(links)} catgirls!')
        await fill_notify.edit(embed=filler_done)
    image_url = random.choice(links)
    if image_url.startswith('//'):
        image_url = 'https:' + image_url
    embed = discord.Embed(color=0xff6699)
    icon_url = 'http://3.bp.blogspot.com/_SUox58HNUCI/SxtiKLuB7VI/AAAAAAAAA08/s_st-jZnavI/s400/Azunyan+fish.jpg'
    embed.set_author(name='Nyaa~', icon_url=icon_url, url=image_url)
    embed.set_image(url=image_url)
    await message.channel.send(None, embed=embed)
