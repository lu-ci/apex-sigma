import aiohttp
import lxml.html as l

async def grab_image(name):
    base_url = 'http://warframe.wikia.com/wiki/Argon_Crystal'
    if ' Blueprint' in name:
        name = name.replace(' Blueprint', '')
    item_url = f'{base_url}/{name}'
    async with aiohttp.ClientSession() as session:
        async with session.get(item_url) as data:
            page_data = await data.read()
    root = l.fromstring(page_data)
    img_object = root.cssselect('.image-thumbnail')[0]
    img_url = img_object.attrib['href']
    return img_url
