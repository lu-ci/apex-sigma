import requests
import discord


async def yomomma(cmd, message, args):
    resource = 'http://api.yomomma.info/'
    data = requests.get(resource).json()
    joke = data['joke']
    if not joke.endswith('.'):
        joke += '.'
    embed = discord.Embed(color=0x1abc9c)
    embed.add_field(name='😂 A Yo Momma Joke', value='```\n' + joke + '\n```')
    await cmd.bot.send_message(message.channel, None, embed=embed)
