from sigma.core.utils import user_avatar
from PIL import Image
from io import BytesIO
import aiohttp
import discord
import os


async def rategirl(cmd, message, args):
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    resize = True
    if args:
        if args[-1].lower() == 'large':
            resize = False
    size_x = 1355
    size_y = 1226
    min_x = 200
    min_y = 1044
    max_x = 1155
    max_y = 182
    spc_x = max_x - min_x
    spc_y = min_y - max_y
    output_location = f'cache/hcz_{message.id}.png'
    with Image.open(cmd.resource('rate/crazy_hot_chart.png')) as chart:
        if target.bot:
            perc_x = '91'
            perc_y = '05'
        else:
            target_data = {'UserID': target.id}
            lookup = cmd.db.find_one('HotCrazyOverrides', target_data)
            if lookup:
                hot_value = lookup['HotValue']
                crazy_value = lookup['CrazyValue']
                if hot_value < 10:
                    hot_value = f'0{hot_value}'
                else:
                    hot_value = str(hot_value)
                if crazy_value < 10:
                    crazy_value = f'0{crazy_value}'
                else:
                    crazy_value = str(crazy_value)
                perc_x = hot_value
                perc_y = crazy_value
            else:
                perc_x = str(target.id)[6] + str(target.id)[9]
                perc_y = str(target.id)[12] + str(target.id)[3]
        loc_x = int(spc_x * (float(f'0.{perc_x}')))
        loc_y = int(spc_y * (1 - (float(f'0.{perc_y}'))))
        ava_x = loc_x + 250
        ava_y = loc_y + 108
        ind_x = loc_x + 175
        ind_y = loc_y + 108
        ava_size = (145, 145)
        user_ava = user_avatar(target)
        async with aiohttp.ClientSession() as session:
            async with session.get(user_ava) as data:
                image_data = await data.read()
                user_ava = BytesIO(image_data)
                with Image.open(user_ava) as user_ava:
                    user_ava = user_ava.resize(ava_size, Image.ANTIALIAS)
                    chart.paste(user_ava, (ava_x, ava_y))
        with Image.open(cmd.resource('rate/user_indicator.png')) as indicator:
            chart.paste(indicator, (ind_x, ind_y), indicator)
        if resize:
            chart = chart.resize((size_x // 2, size_y // 2), Image.ANTIALIAS)
        chart.save(output_location)
    with open(output_location, 'rb') as resp_img:
        resp = discord.File(resp_img)
        await message.channel.send(file=resp)
    os.remove(output_location)
