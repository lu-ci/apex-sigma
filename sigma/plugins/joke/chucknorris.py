import requests
import discord


async def chucknorris(cmd, message, args):
    embed = discord.Embed(color=0x1abc9c)
    cmd.db.add_stats('CancerCount')
    joke_url = 'https://api.chucknorris.io/jokes/random'
    joke_json = requests.get(joke_url).json()
    joke = joke_json['value']
    out = '```yaml\n\"'
    out += joke
    out += '\"\n```'
    embed.add_field(name='A Chuck Norris Joke', value=out)
    await cmd.bot.send_message(message.channel, None, embed=embed)
