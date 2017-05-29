import json
import ftfy
import random
import aiohttp
import discord
from lxml import html as l


async def joke(cmd, message, args):
    randomizer = random.randint(1, 6644)
    joke_url = f'http://jokes.cc.com/feeds/random/{randomizer}'
    async with aiohttp.ClientSession() as session:
        async with session.get(joke_url) as data:
            joke_json = await data.read()
            joke_json = json.loads(joke_json)
            joke_page_url = joke_json['0']['url']
    async with aiohttp.ClientSession() as session:
        async with session.get(joke_page_url) as data:
            page_data = await data.text()
    root = l.fromstring(page_data)
    content = root.cssselect('.content_wrap')[0]
    joke_text = ''
    for element in content.cssselect('p'):
        if element.text != '' and element.text != '\n':
            joke_text += f'\n{element.text}'
    while '  ' in joke_text:
        joke_text = joke_text.replace('  ', ' ')
    joke_text = ftfy.fix_text(joke_text)
    embed = discord.Embed(color=0x1abc9c)
    embed.add_field(name='😆 Have A Random Joke', value='\n```' + joke_text + '\n```')
    await message.channel.send(None, embed=embed)
