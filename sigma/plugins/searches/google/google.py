import aiohttp
import discord
import random
from config import GoogleAPIKey
from config import GoogleCSECX


async def google(cmd, message, args):
    if not args:
        await message.channel.send(cmd.help())
        return
    else:
        search = ' '.join(args)
        url = 'https://www.googleapis.com/customsearch/v1?q=' + search + '&cx=' + GoogleCSECX + '&key=' + GoogleAPIKey
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                results = await data.json()
        google_colors = [0x4285f4, 0x34a853, 0xfbbc05, 0xea4335, 0x00a1f1, 0x7cbb00, 0xffbb00, 0xf65314]
        embed_color = random.choice(google_colors)
        try:
            title = results['items'][0]['title']
            url = results['items'][0]['link']
            embed = discord.Embed(color=embed_color)
            embed.set_author(name='Google', icon_url='https://avatars2.githubusercontent.com/u/1342004?v=3&s=400',
                             url='https://www.google.com/search?q=' + search)
            embed.add_field(name=title, value='[**Link Here**](' + url + ')')
            await message.channel.send(None, embed=embed)
        except:
            embed = discord.Embed(color=0xDB0000, title='❗ Daily Limit Reached.')
            embed.set_footer(text='Google limits this API feature, and we hit that limit.')
            await message.channel.send(None, embed=embed)
