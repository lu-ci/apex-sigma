import requests


async def joke(cmd, message, args):
    joke_url = 'http://tambal.azurewebsites.net/joke/random'
    joke_json = requests.get(joke_url).json()
    joke = joke_json['joke']
    await cmd.bot.send_message(message.channel, 'Here, have this!\n```' + joke + '\n```')
