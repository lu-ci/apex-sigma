import requests
import random
from lxml import html

async def safebooru(cmd, message, args):
    if not args:
        tag = 'cute'
    else:
        tag = ' '.join(args)
        tag = tag.replace(' ', '+')
    try:
        resource = 'http://safebooru.org/index.php?page=dapi&s=post&q=index&tags=' + tag
        data = requests.get(resource)
        posts = html.fromstring(data.content)
        choice = random.choice(posts)
        await cmd.bot.send_message(message.channel, choice.attrib['file_url'])
    except Exception as e:
        cmd.log.error(e)
        await cmd.bot.send_message(message.channel, str(e))
