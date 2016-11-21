import random
import requests
from lxml import html

async def hentai(cmd, message, args):
    if not args:
        tag = 'nude'
    else:
        tag = ' '.join(args)
        tag = tag.replace(' ', '+')
    try:
        # Danbooru
        try:
            dan_resource = 'https://danbooru.donmai.us/post/index.json?&tags=' + tag
            dan_file_url_base = 'https://danbooru.donmai.us'
            dan_data = requests.get(dan_resource).json()
            dan_chosen_post = random.choice(dan_data)
            dan_post_url = dan_chosen_post['file_url']
            dan_url = dan_file_url_base + dan_post_url
        except:
            dan_url = 'Nothing on Danbooru'
        # Gelbooru
        try:
            gelbooru_url = 'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=' + tag
            data = requests.get(gelbooru_url)
            posts = html.fromstring(data.content)
            choice = random.choice(posts)
            gel_url = choice.attrib['file_url']
        except:
            gel_url = 'Nothing on Gelbooru'
        # Rule34
        try:
            r34_url = 'http://rule34.xxx/index.php?page=dapi&s=post&q=index&tags=' + tag
            data = requests.get(r34_url)
            posts = html.fromstring(data.content)
            choice = random.choice(posts)
            r34_url = str(choice.attrib['file_url']).replace('//img', 'http://img')
        except:
            r34_url = 'Nothing on Gelbooru'
        # Final
        out_text = 'Danbooru: ' + dan_url + '\nGelbooru: ' + gel_url + '\nRule34: ' + r34_url
        await cmd.bot.send_message(message.channel, out_text)
    except Exception as e:
        cmd.log.error(e)
        await cmd.bot.send_message(message.channel, str(e))
