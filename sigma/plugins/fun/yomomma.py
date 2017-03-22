import aiohttp
import discord
import json

async def yomomma(cmd, message, args):
    resource = 'http://api.yomomma.info/'
    async with aiohttp.ClientSession() as session:
        async with session.get(resource) as data:
            data = await data.read()
            data = json.loads(data)
    joke = data['joke']
    if not joke.endswith('.'):
        joke += '.'
    embed = discord.Embed(color=0x1abc9c)
    embed.add_field(name='😂 A Yo Momma Joke', value='```\n' + joke + '\n```')
    await cmd.bot.send_message(message.channel, None, embed=embed)
