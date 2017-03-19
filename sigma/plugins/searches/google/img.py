import aiohttp
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
        url = 'https://www.googleapis.com/customsearch/v1?q=' + search + '&cx=' + GoogleCSECX + '&searchType=image&safe=high' + '&key=' + GoogleAPIKey
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                results = await data.json()
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
            embed = discord.Embed(color=0xDB0000, title='❗ Daily Limit Reached.')
            embed.set_footer(text='Google limits this API feature, and we hit that limit.')
            await cmd.bot.send_message(message.channel, None, embed=embed)
