import requests
from config import CatAPIKey
from lxml import html
import random


async def cat(cmd, message, args):
    out_text = ''
    raw_page = requests.get('http://thecatapi.com/api/images/get?format=xml&results_per_page=100&api_key=' + CatAPIKey)
    results = html.fromstring(raw_page.content)[0][0]
    choice = random.choice(results)
    image_url = str(choice[0].text)
    out_text += image_url
    if CatAPIKey == '':
        out_text += '\n**Warning** No Api Key Is Present. Use of command is limited to 1000 per day.'
    await cmd.bot.send_message(message.channel, out_text)
