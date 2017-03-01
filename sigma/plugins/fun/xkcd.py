import random
import aiohttp
import discord


async def xkcd(cmd, message, args):
    comic_no = str(random.randint(1, 1724))
    joke_url = 'http://xkcd.com/' + comic_no + '/info.0.json'
    async with aiohttp.ClientSession() as session:
        async with session.get(joke_url) as data:
            joke_json = await data.json()
    image_url = joke_json['img']
    embed = discord.Embed(color=0x1abc9c, title='🚽 An XKCD Comic')
    embed.set_image(url=image_url)
    await cmd.bot.send_message(message.channel, None, embed=embed)
