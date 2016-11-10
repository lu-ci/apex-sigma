import requests


async def chucknoris(cmd, message, args):
    joke_url = 'https://api.chucknorris.io/jokes/random'
    joke_json = requests.get(joke_url).json()
    joke = joke_json['value']
    out = '```yaml\n\"'
    out += joke
    out += '\"\n```'
    await cmd.bot.send_message(message.channel, out)
