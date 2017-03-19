import aiohttp
import discord
from config import Food2ForkAPIKey


async def recipe(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    search = ' '.join(args)
    url = 'http://food2fork.com/api/search?key=' + Food2ForkAPIKey + '&q=' + search
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as data:
            search_data = await data.json()
    count = search_data['count']
    if count == 0:
        embed = discord.Embed(color=0x696969, title='🔍 No results were found for that, sorry.')
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    else:
        info = search_data['recipes'][0]
        title = info['title']
        source = info['publisher']
        source_url = info['source_url']
        image_url = info['image_url']
        publisher_url = info['publisher_url']
        embed = discord.Embed(color=0x1abc9c)
        embed.set_author(name=source, url=publisher_url,
                         icon_url='https://cdn0.iconfinder.com/data/icons/kameleon-free-pack-rounded/110/Food-Dome-512.png')
        embed.add_field(name=title, value='[**Recipe Here**](' + source_url + ')')
        embed.set_image(url=image_url)
        await cmd.bot.send_message(message.channel, None, embed=embed)
