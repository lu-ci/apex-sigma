import aiohttp
import json

items = {}


async def get_all_items():
    if not items:
        url = 'http://warframe.market/api/get_all_items_v2'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                api_data = await data.read()
                api_data = json.loads(api_data)
        for item in api_data:
            items.update({item['item_name'].lower().replace(' ', '_'): item})
    return items
