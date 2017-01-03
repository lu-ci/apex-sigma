import requests
import random
from config import GoogleAPIKey
from config import GoogleCSECX


async def img(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    else:
        search = ' '.join(args)
        results = requests.get(
            'https://www.googleapis.com/customsearch/v1?q=' + search + '&cx=' + GoogleCSECX + '&searchType=image' + '&key=' + GoogleAPIKey).json()
        try:
            result_items = results['items']
            choice = random.choice(result_items)
            title = choice['title']
            url = choice['link']
            out = '`' + title + '`: \n' + url
            await cmd.bot.send_message(message.channel, out)
        except Exception as e:
            cmd.log.error(e)
            await cmd.bot.send_message(message.channel, 'Could not parse the results. The daily limit might have been reached.')
