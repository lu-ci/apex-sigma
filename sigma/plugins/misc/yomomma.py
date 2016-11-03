import requests


async def yomomma(cmd, message, args):
    try:
        resource = 'http://api.yomomma.info/'
        data = requests.get(resource).json()
        joke = data['joke']
        if not joke.endswith('.'):
            joke += '.'
        await cmd.reply(joke)
    except Exception as e:
        cmd.log.error(e)
        await cmd.reply(str(e))
