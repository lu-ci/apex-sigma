import aiohttp
import lxml.html as l

async def grab_image(name):
    base_url = 'http://warframe.wikia.com/wiki'
    if ' Blueprint' in name:
        name = name.replace(' Blueprint', '')
    name = name.replace(' ', '_')
    check_name = name.split('_')
    try:
        int(check_name[0])
        resource = True
    except:
        resource = False
    if resource:
        name = '_'.join(check_name[1:])
    item_url = f'{base_url}/{name}'
    async with aiohttp.ClientSession() as session:
        async with session.get(item_url) as data:
            page_data = await data.read()
    root = l.fromstring(page_data)
    img_object = root.cssselect('.image')[0]
    img_url = img_object.attrib['href']
    return img_url
