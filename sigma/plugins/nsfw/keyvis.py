import random
import discord
from .visual_novels import key_vn_list


async def keyvis(cmd, message, args):
    if not args:
        choice = random.choice(list(key_vn_list.keys()))
    else:
        choice = [x.lower() for x in args][0]
    try:
        item = key_vn_list[choice]
    except KeyError:
        embed = discord.Embed(color=0x696969, title='🔍 Nothing found for {:s}...'.format(
            ' '.join(['`{:s}`'.format(x) for x in args])))
        await message.channel.send(None, embed=embed)
        return

    ran_image_number = random.randint(1, item[1])
    ran_number_length = len(str(ran_image_number))

    url_base = 'https://cgv.blicky.net'
    image_url = '{:s}/{:s}/{:s}{:d}.jpg'.format(
        url_base, item[0], '0000'[:-ran_number_length], ran_image_number)
    embed = discord.Embed(color=0x9933FF)
    embed.set_image(url=image_url)
    await message.channel.send(None, embed=embed)
