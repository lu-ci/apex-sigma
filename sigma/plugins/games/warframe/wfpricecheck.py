import json
import aiohttp
import discord
from .nodes.image_grabber import alt_grab_image, grab_image
from .nodes.market import get_all_items

plat_img = 'http://i.imgur.com/wa6J9bz.png'
cuttables = ['blueprint', 'set', 'barrel', 'stock', 'receiver', 'hilt', 'pouch', 'blade', 'guard']


async def wfpricecheck(cmd, message, args):
    if args:
        lookup = '_'.join(args).lower()
        lookup_pretty = ' '.join(args).title()
        items = await get_all_items()
        if lookup in items:
            item_type = items[lookup]['item_type']
            full_item_name = items[lookup]['item_name']
            api_url = f'https://warframe.market/api/get_orders/{item_type}/{full_item_name}'
            cut = False
            for arg in args:
                if arg.lower() in cuttables:
                    cut = True
                    break
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as data:
                    api_data = await data.read()
                    api_data = json.loads(api_data)
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
                if not lowest:
                    response = discord.Embed(color=0x696969, title=f'🔍 {lookup_pretty} Found But No Active Sales.')
                    await message.channel.send(embed=response)
                    return
                item_desc = f'Price: {lowest["price"]}p'
                item_desc += f'\nAmount: {lowest["count"]}'
                item_desc += f'\nSeller: {lowest["ingame_name"]}'
                response = discord.Embed(color=0xFFCC66)
                response.add_field(name=f'{lookup_pretty}', value=item_desc)
                try:
                    item_img = await alt_grab_image(lookup_pretty, cut)
                    if item_img.startswith('http'):
                        first_img_fail = False
                    else:
                        first_img_fail = True
                except:
                    item_img = None
                    first_img_fail = True
                if first_img_fail:
                    try:
                        item_img = await grab_image(lookup_pretty, cut)
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
            response = discord.Embed(color=0x696969, title=f'🔍 {lookup_pretty} Not Found.')
        await message.channel.send(embed=response)
