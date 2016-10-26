import requests
import random
from lxml import html


async def gelbooru(cmd, message, args):
    tags = '+'.join(args)

    try:
        if tags == '':
            tags = 'nude'

        gelbooru_url = 'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=' + tags
        data = requests.get(gelbooru_url)
        posts = html.fromstring(data.content)
        choice = random.choice(posts)

        await cmd.reply(choice.attrib['file_url'])
    except Exception as e:
        cmd.log.error(e)
        await cmd.reply('Nothing found...')
