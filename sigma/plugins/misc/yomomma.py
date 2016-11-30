import requests


async def yomomma(cmd, message, args):
    try:
        resource = 'http://api.yomomma.info/'
        data = requests.get(resource).json()
        joke = data['joke']
        if not joke.endswith('.'):
            joke += '.'
        await cmd.bot.send_message(message.channel, joke)
    except Exception as e:
        cmd.log.error(e)
        await cmd.bot.send_message(message.channel, str(e))
