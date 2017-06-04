import aiohttp
import discord
import random
from lxml import html


async def rule34(cmd, message, args):
    tags = '+'.join(args)

    try:
        if not tags:
            tags = 'nude'

        r34_url = 'https://rule34.xxx/index.php?page=dapi&s=post&q=index&tags=' + tags
        async with aiohttp.ClientSession() as session:
            async with session.get(r34_url) as data:
                data = await data.read()
        posts = html.fromstring(data)
        choice = random.choice(posts)
        img_url = choice.attrib['file_url']
        if not img_url.startswith('http'):
            img_url = f"https:{choice.attrib['file_url']}"
        icon_url = 'https://i.imgur.com/63GGrmG.png'
        post_url = f'https://rule34.xxx/index.php?page=post&s=view&id={choice.attrib["id"]}'
        embed = discord.Embed(color=0xaae5a3)
        embed.set_author(name='Rule 34', url=post_url, icon_url=icon_url)
        embed.set_image(url=img_url)
        embed.set_footer(
            text=f'Score: {choice.attrib["score"]} | Size: {choice.attrib["width"]}x{choice.attrib["height"]}')
        await message.channel.send(None, embed=embed)
    except:
        embed = discord.Embed(color=0x696969, title='🔍 Search for ' + tags + ' yielded no results.')
        await message.channel.send(None, embed=embed)
