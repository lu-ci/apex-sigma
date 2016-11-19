import random
import requests


async def xkcd(cmd, message, args):
    comic_no = str(random.randint(1, 1724))
    joke_url = 'http://xkcd.com/' + comic_no + '/info.0.json'
    joke_json = requests.get(joke_url).json()
    image_url = joke_json['img']
    await cmd.bot.send_message(message.channel, image_url)
