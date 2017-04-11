import aiohttp
import discord
import random
from lxml import html


async def gelbooru(cmd, message, args):
    tags = '+'.join(args)

    try:
        if tags == '':
            tags = 'nude'
        gelbooru_url = 'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=' + tags
        async with aiohttp.ClientSession() as session:
            async with session.get(gelbooru_url) as data:
                data = await data.read()
        posts = html.fromstring(data)
        choice = random.choice(posts)
        img_url = choice.attrib['file_url']
        if not img_url.startswith('http'):
            img_url = f"https:{choice.attrib['file_url']}"
        print()
        embed = discord.Embed(color=0x9933FF)
        embed.set_image(url=img_url)
        await message.channel.send(None, embed=embed)
    except Exception as e:
        cmd.log.error(e)
        embed = discord.Embed(color=0x696969, title='🔍 Search for ' + tags + ' yielded no results.')
        embed.set_footer(
            text='Remember to replace spaces in tags with an underscore, as a space separates multiple tags')
        await message.channel.send(None, embed=embed)
