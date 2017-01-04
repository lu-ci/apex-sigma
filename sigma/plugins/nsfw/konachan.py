import requests
import discord
import random


async def konachan(cmd, message, args):
    url_base = 'https://konachan.com/post.json?limit=100&tags='
    if not args:
        tags = 'nude'
    else:
        tags = '+'.join(args)
    url = url_base + tags
    data = requests.get(url).json()
    if len(data) == 0:
        embed = discord.Embed(color=0x696969, title=':mag: No results.')
    else:
        post = random.choice(data)
        image_url = 'http:' + post['file_url']
        embed = discord.Embed(color=0x9933FF)
        embed.set_image(url=image_url)
    await cmd.bot.send_message(message.channel, None, embed=embed)
