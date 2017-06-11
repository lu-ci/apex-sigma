import json
import aiohttp
import discord
from .nodes.image_grabber import alt_grab_image, grab_image
from .nodes.market import get_all_items

plat_img = 'http://i.imgur.com/wa6J9bz.png'
cuttables = ['set', 'barrel', 'stock', 'receiver', 'hilt', 'pouch', 'blade', 'guard',
             'neuroptics', 'chassis', 'systems', 'wings', 'harness', 'gauntlet']


async def grab_item_image(lookup, cut):
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
    return item_img


async def wfpricecheck(cmd, message, args):
    initial_response = discord.Embed(color=0xFFCC66, title='🔬 Processing...')
    init_resp_msg = await message.channel.send(embed=initial_response)
    if args:
        lookup = '_'.join(args).lower()
        lookup_pretty = ' '.join(args).title()
        items = await get_all_items()
        img_grabbed = False
        found = 0
        response = discord.Embed(color=0xFFCC66)
        response.set_author(name='Warframe Market Search', icon_url='https://i.imgur.com/VNwpelI.png')
        for key in items:
            if lookup in key:
                found += 1
                item_type = items[key]['item_type']
                full_item_name = items[key]['item_name']
                api_url = f'https://warframe.market/api/get_orders/{item_type}/{full_item_name}'
                cut = False
                for arg in full_item_name.split(' '):
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
                    if lowest:
                        item_desc = f'Price: {lowest["price"]}p'
                        item_desc += f'\nAmount: {lowest["count"]}'
                        item_desc += f'\nSeller: {lowest["ingame_name"]}'
                    else:
                        item_desc = 'No Data'
                    response.add_field(name=f'{full_item_name}', value=item_desc)
                    if not img_grabbed:
                            item_img = await grab_image(full_item_name, cut)
                            response.set_thumbnail(url=item_img)
                            img_grabbed = True
        if found == 0:
            response = discord.Embed(color=0x696969, title=f'🔍 {lookup_pretty} Not Found.')
    else:
        response = discord.Embed(color=0x696969, title=f'🔍 Nothing Inputted.')
    try:
        await init_resp_msg.edit(embed=response)
    except:
        pass
