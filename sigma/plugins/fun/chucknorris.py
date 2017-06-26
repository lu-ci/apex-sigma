import aiohttp
import discord


async def chucknorris(cmd, message, args):
    embed = discord.Embed(color=0x1abc9c)
    joke_url = 'https://api.chucknorris.io/jokes/random'
    async with aiohttp.ClientSession() as session:
        async with session.get(joke_url) as data:
            joke_json = await data.json()
    joke = joke_json['value']
    out = '```\n'
    out += joke
    out += '\n```'
    embed.add_field(name='💪 A Chuck Norris Joke', value=out)
    await message.channel.send(None, embed=embed)
