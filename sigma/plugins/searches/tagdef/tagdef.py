import requests
from config import MashapeKey

async def tagdef(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
    else:
        hashtag = (' '.join(args)).replace('#', '')
        try:
            url = "https://tagdef.p.mashape.com/one." + hashtag + '.json'
            headers = {'X-Mashape-Key': MashapeKey, 'Accept': 'text/plain'}
            response = requests.get(url, headers=headers).json()
            result = response['defs']['def']['text']
            out_text = 'The definition for **#' + hashtag + '**:'
            out_text += '\n```\n' + result + '\n```'
            await cmd.bot.send_message(message.channel, out_text)
        except Exception as e:
            cmd.log.error(e)
            await cmd.bot.send_message(message.channel, 'The Definition for **#' + hashtag + '** was not found.')
