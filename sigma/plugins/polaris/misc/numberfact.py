import random
import requests


async def numberfact(cmd, message, args):
    types = ['trivia', 'date', 'math', 'year']
    ran_type = random.choice(types)
    if not args:
        url = 'http://numbersapi.com/random/' + ran_type + '?json'
    else:
        number = args[0]
        if len(args) > 1:
            fact_type = args[1]
            fact_type = fact_type.lower()
            if fact_type not in types:
                await cmd.bot.send_message(message.channel, 'Invalid fact type.')
                return
        else:
            fact_type = ran_type
        url = 'http://numbersapi.com/' + number + '/' + fact_type + '?json'
    try:
        data = requests.get(url).json()
        fact = data['text']
        await cmd.bot.send_message(message.channel, '```\n' + fact + '\n```')
    except Exception as e:
        cmd.log.error(e)
        await cmd.bot.send_message(message.channel, 'We could not parse the page.')
