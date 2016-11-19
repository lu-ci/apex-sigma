import requests


async def catfact(cmd, message, args):
    try:
        resource = 'http://catfacts-api.appspot.com/api/facts'
        data = requests.get(resource).json()
        fact = data['facts'][0]
        await cmd.bot.send_message(message.channel, 'Did you know:\n```\n' + fact + '\n```')
    except Exception as e:
        cmd.log.error(e)
        await cmd.bot.send_message(message.channel, str(e))
