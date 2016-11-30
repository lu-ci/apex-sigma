import requests


async def ronswanson(cmd, message, args):
    api_url = 'http://ron-swanson-quotes.herokuapp.com/v2/quotes'
    data = requests.get(api_url).json()
    joke = data[0]
    out = '```yaml\n\"'
    out += joke
    out += '\"\n```'
    await cmd.bot.send_message(message.channel, out)
