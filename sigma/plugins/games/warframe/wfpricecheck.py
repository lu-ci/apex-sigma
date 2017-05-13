import json
import aiohttp
import discord
from .nodes.image_grabber import alt_grab_image, grab_image

plat_img = 'http://i.imgur.com/wa6J9bz.png'

async def wfpricecheck(cmd, message, args):
    if args:
        if args[-1].lower() == 'mod':
            cut = False
            lookup = ' '.join(args[:-1]).lower().title()
            api_url = f'https://warframe.market/api/get_orders/Mod/{lookup}'
        elif args[-1].lower() == 'set':
            cut = True
            lookup = ' '.join(args).lower().title()
            api_url = f'https://warframe.market/api/get_orders/Set/{lookup}'
        else:
            lookup = ' '.join(args).lower().title()
            if 'blueprint' in lookup.lower():
                cut = False
            else:
                cut = True
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
                    if not item['ingame_name'].startswith('('):
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
                item_img = await alt_grab_image(lookup, cut)
                if item_img.startswith('http'):
                    first_img_fail = False
                else:
                    first_img_fail = True
            except:
                item_img = None
                first_img_fail = True
            if first_img_fail:
                try:
                    item_img = await grab_image(lookup, cut)
                    if item_img.startswith('http'):
                        final_img_fail = False
                    else:
                        final_img_fail = True
                except:
                    final_img_fail = True
            else:
                final_img_fail = False
            if final_img_fail:
                item_img = plat_img
            response.set_thumbnail(url=item_img)
        else:
            response = discord.Embed(color=0x696969, title=f'🔍 {lookup} Not Found.')
        await message.channel.send(embed=response)
