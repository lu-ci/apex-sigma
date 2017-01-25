import requests
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
    data = requests.get(resource)
    posts = html.fromstring(data.content)
    choice = random.choice(posts)
    image_url = choice.attrib['file_url']
    if image_url.startswith('//'):
        image_url = 'http:' + image_url
    embed = discord.Embed(color=0xff6699)
    embed.set_image(url=image_url)
    await cmd.bot.send_message(message.channel, None, embed=embed)
