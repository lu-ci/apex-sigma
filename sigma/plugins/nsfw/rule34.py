import requests
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

        await cmd.bot.send_message(message.channel, str(choice.attrib['file_url']).replace('//img', 'http://img'))
    except Exception as e:
        cmd.log.info(e)
        await cmd.bot.send_message(message.channel, 'Nothing found...')
