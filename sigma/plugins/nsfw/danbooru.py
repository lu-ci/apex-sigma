import aiohttp
import random
import discord

links = {}

async def get_dan_post(tag):
    file_url_base = 'https://danbooru.donmai.us'
    if tag not in links:
        need_filling = True
    else:
        if len(links[tag]) == 0:
            need_filling = True
        else:
            need_filling = False
    if need_filling:
        resource = 'https://danbooru.donmai.us/post/index.json?&tags=' + tag
        async with aiohttp.ClientSession() as session:
            async with session.get(resource) as data:
                data = await data.json()
        temp_list = []
        for post in data:
            if 'file_url' in post:
                temp_list.append(post['file_url'])
        links.update({tag: temp_list})
    random.shuffle(links[tag])
    img_url = links[tag].pop()
    full_url = file_url_base + img_url
    return full_url


async def danbooru(cmd, message, args):
    if not args:
        tag = 'nude'
    else:
        tag = ' '.join(args).lower()
        tag = tag.replace(' ', '+')
    image_url = await get_dan_post(tag)
    if not image_url:
        response = discord.Embed(color=0x696969, title='🔍 Search for ' + tag + ' yielded no results.')
        response.set_footer(
            text='Remember to replace spaces in tags with an underscore, as a space separates multiple tags')
    else:
        response = discord.Embed(color=0x9933FF)
        response.set_image(url=image_url)
    await message.channel.send(None, embed=response)
