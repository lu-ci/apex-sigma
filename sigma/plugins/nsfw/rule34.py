import requests
import discord
import random
from lxml import html


async def rule34(cmd, message, args):
    tags = '+'.join(args)

    try:
        if not tags:
            tags = 'nude'

        r34_url = 'http://rule34.xxx/index.php?page=dapi&s=post&q=index&tags=' + tags
        data = requests.get(r34_url)
        posts = html.fromstring(data.content)
        choice = random.choice(posts)
        url = str(choice.attrib['file_url']).replace('//', 'http://')
        embed = discord.Embed(color=0x9933FF)
        embed.set_image(url=url)
        await cmd.bot.send_message(message.channel, None, embed=embed)
    except Exception as e:
        cmd.log.info(e)
        embed = discord.Embed(color=0x696969, title=':mag: Search for ' + tags + ' yielded no results.')
        embed.set_footer(
            text='Remember to replace spaces in tags with an underscore, as a space separates multiple tags')
        await cmd.bot.send_message(message.channel, None, embed=embed)
