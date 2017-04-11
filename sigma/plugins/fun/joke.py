import aiohttp
import discord


async def joke(cmd, message, args):
    joke_url = 'http://tambal.azurewebsites.net/joke/random'
    async with aiohttp.ClientSession() as session:
        async with session.get(joke_url) as data:
            joke_json = await data.json()
    joke_text = joke_json['joke']
    embed = discord.Embed(color=0x1abc9c)
    embed.add_field(name='😆 Have A Random Joke', value='\n```' + joke_text + '\n```')
    await message.channel.send(None, embed=embed)
