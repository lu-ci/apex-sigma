import random
import discord
import requests


async def butts(cmd, message, args):
    api_base = 'http://api.obutts.ru/butts/'
    number = random.randint(1, 4296)
    url_api = api_base + str(number)
    data = requests.get(url_api).json()[0]
    image_url = 'http://media.obutts.ru/' + data['preview']
    embed = discord.Embed(color=0x9933FF)
    embed.set_image(url=image_url)
    await cmd.bot.send_message(message.channel, None, embed=embed)
