import requests
import discord
from config import MashapeKey


async def tagdef(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    hashtag = (' '.join(args)).replace('#', '')
    url = "https://tagdef.p.mashape.com/one." + hashtag + '.json'
    headers = {'X-Mashape-Key': MashapeKey, 'Accept': 'text/plain'}
    response = requests.get(url, headers=headers).json()
    result = response['defs']['def']['text']
    embed = discord.Embed(color=0x1abc9c)
    embed.add_field(name='#⃣ Definition of `#' + hashtag + '`', value='```\n' + result + '\n```')
    await cmd.bot.send_message(message.channel, None, embed=embed)
