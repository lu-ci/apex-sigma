import requests
from config import CatAPIKey
from lxml import html
import random
import discord


async def cat(cmd, message, args):
    raw_page = requests.get('http://thecatapi.com/api/images/get?format=xml&results_per_page=100&api_key=' + CatAPIKey)
    results = html.fromstring(raw_page.content)[0][0]
    choice = random.choice(results)
    image_url = str(choice[0].text)
    embed = discord.Embed(color=0x1abc9c)
    embed.set_image(url=image_url)
    await cmd.bot.send_message(message.channel, None, embed=embed)
