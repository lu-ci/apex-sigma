import discord
import random
from lxml import html
import aiohttp


async def e621(cmd, message, args):
    url_base = 'http://e621.net/post/index.xml'
    if args:
        url = url_base + '?tags=' + '+'.join(args)
    else:
        url = url_base + '?tags=nude'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as data:
            data = await data.text()
    posts = html.fromstring(data)
    post = random.choice(posts)
    image_url = post.find('file_url').text
    embed = discord.Embed(color=0x9933FF)
    embed.set_image(url=image_url)
    await cmd.bot.send_message(message.channel, None, embed=embed)
