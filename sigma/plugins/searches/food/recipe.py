import json
import aiohttp
import discord
from config import Food2ForkAPIKey


async def recipe(cmd, message, args):
    if not args:
        await message.channel.send(cmd.help())
        return
    search = ' '.join(args)
    url = 'http://food2fork.com/api/search?key=' + Food2ForkAPIKey + '&q=' + search
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as data:
            search_data = await data.read()
            search_data = json.loads(search_data)
    count = search_data['count']
    if count == 0:
        embed = discord.Embed(color=0x696969, title='🔍 No results were found for that, sorry.')
        await message.channel.send(None, embed=embed)
        return
    else:
        info = search_data['recipes'][0]
        title = info['title']
        source = info['publisher']
        source_url = info['source_url']
        image_url = info['image_url']
        publisher_url = info['publisher_url']
        embed = discord.Embed(color=0x1abc9c)
        embed.set_author(name=source, url=publisher_url, icon_url='https://i.imgur.com/RH8LNdQ.png')
        embed.add_field(name=title, value='[**Recipe Here**](' + source_url + ')')
        embed.set_thumbnail(url=image_url)
        await message.channel.send(None, embed=embed)
