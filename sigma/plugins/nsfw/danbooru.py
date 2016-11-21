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
        links = []
        for post in data:
            try:
                links.append(post['file_url'])
            except:
                pass
        if len(links) == 0:
            await cmd.bot.send_message(message.channel, 'Nothing found...')
            return
        chosen_post = random.choice(links)
        url = file_url_base + chosen_post
        await cmd.bot.send_message(message.channel, url)
    except Exception as e:
        cmd.log.error(e)
        await cmd.bot.send_message(message.channel, str(e))

