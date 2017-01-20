import requests
import random
import discord
from config import GoogleAPIKey
from config import GoogleCSECX


async def img(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    else:
        search = ' '.join(args)
        results = requests.get(
            'https://www.googleapis.com/customsearch/v1?q=' + search + '&cx=' + GoogleCSECX + '&searchType=image' + '&key=' + GoogleAPIKey).json()
        try:
            result_items = results['items']
            choice = random.choice(result_items)
            title = choice['title']
            if len(title) > 48:
                title = title[:48] + '...'
            url = choice['link']
            embed = discord.Embed(color=0x1abc9c, title=title)
            embed.set_image(url=url)
            await cmd.bot.send_message(message.channel, None, embed=embed)
        except Exception as e:
            cmd.log.error(e)
            embed = discord.Embed(color=0xDB0000)
            embed.add_field(name=':exclamation: Error',
                            value='Could not parse the results. The daily limit might have been reached.')
            await cmd.bot.send_message(message.channel, None, embed=embed)
