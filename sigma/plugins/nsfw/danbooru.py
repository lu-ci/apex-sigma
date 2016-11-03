import requests
import random

async def danbooru(cmd, message, args):
    if not args:
        tag = 'nude'
    else:
        tag = ' '.join(args)
        tag = tag.replace(' ', '+')
    try:
        resource = 'https://danbooru.donmai.us/post/index.json?&tags=' + tag
        file_url_base = 'https://danbooru.donmai.us'
        data = requests.get(resource).json()
        chosen_post = random.choice(data)
        post_url = chosen_post['file_url']
        url = file_url_base + post_url
        await cmd.reply(url)
    except Exception as e:
        cmd.log.error(e)
        await cmd.reply(str(e))

