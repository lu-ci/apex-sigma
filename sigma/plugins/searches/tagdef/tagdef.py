import requests
from config import MashapeKey

async def tagdef(cmd, message, args):
    if not args:
        await cmd.reply(cmd.help())
    else:
        hashtag = (' '.join(args)).replace('#', '')
        try:
            url = "https://tagdef.p.mashape.com/one." + hashtag + '.json'
            headers = {'X-Mashape-Key': MashapeKey, 'Accept': 'text/plain'}
            response = requests.get(url, headers=headers).json()
            result = response['defs']['def']['text']
            out_text = 'The definition for **#' + hashtag + '**:'
            out_text += '\n```\n' + result + '\n```'
            await cmd.reply(out_text)
        except Exception as e:
            cmd.log.error(e)
            await cmd.reply('The Definition for **#' + hashtag + '** was not found.')
