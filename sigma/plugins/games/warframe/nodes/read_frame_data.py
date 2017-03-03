import aiohttp
import discord
import lxml.html as l


async def read_frame_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as data:
            page = await data.text()
    root = l.fromstring(page)
    drop_tables = root.cssselect('.tabbertab')
    pc_drop_table = drop_tables[0][1]
    item_image = root.cssselect('.pi-image-thumbnail')[0].attrib['src']
    embed = discord.Embed(color=0x0066CC)
    embed.set_thumbnail(url=item_image)
    for row in pc_drop_table:
        row_title = row[0].text.strip()
        row_location = "\n".join([x for x in row[1].itertext()])
        embed.add_field(name=row_title, value=f'```\n{row_location}\n```')
    return embed


async def read_item_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as data:
            page = await data.text()
    root = l.fromstring(page)
    drop_tables = root.cssselect('.tabbertab')
    pc_drop_table = drop_tables[0][1]
    item_image = root.cssselect('.infobox')[0][1][0][0].attrib['href']
    embed = discord.Embed(color=0x0066CC)
    embed.set_thumbnail(url=item_image)
    for row in pc_drop_table:
        row_title = row[0].text
        if not row_title or row_title == 'None':
            row_title = row[0][0].attrib['title']
        row_location = "\n".join([x for x in row[1].itertext()])
        embed.add_field(name=row_title, value=f'```\n{row_location}\n```')
    return embed
