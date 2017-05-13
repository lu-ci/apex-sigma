import json
import aiohttp
import discord
from .nodes.image_grabber import alt_grab_image, grab_image

plat_img = 'http://i.imgur.com/wa6J9bz.png'

async def wfpricecheck(cmd, message, args):
    if args:
        if args[0].lower() == 'mod':
            lookup = ' '.join(args[1:]).lower().title()
            api_url = f'https://warframe.market/api/get_orders/Mod/{lookup}'
        else:
            lookup = ' '.join(args).lower().title()
            api_url = f'https://warframe.market/api/get_orders/Blueprint/{lookup}'
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as data:
                api_data = await data.read()
                api_data = json.loads(api_data)
        if api_data['code'] == 200:
            lowest = None
            listings = api_data['response']['sell']
            for item in listings:
                if item['online_ingame']:
                    if lowest:
                        if lowest['price'] > item['price']:
                            lowest = item
                    else:
                        lowest = item
            item_desc = f'Price: {lowest["price"]}p'
            item_desc += f'\nAmount: {lowest["count"]}'
            item_desc += f'\nSeller: {lowest["ingame_name"]}'
            response = discord.Embed(color=0xFFCC66)
            response.add_field(name=f'{lookup}', value=item_desc)
            try:
                item_img = await alt_grab_image(lookup)
            except:
                try:
                    item_img = await grab_image(lookup)
                except:
                    item_img = plat_img
            if not item_img.startswith('http'):
                item_img = plat_img
            response.set_thumbnail(url=item_img)
        else:
            response = discord.Embed(color=0x696969, title=f'🔍 {lookup} Not Found.')
        await message.channel.send(embed=response)
