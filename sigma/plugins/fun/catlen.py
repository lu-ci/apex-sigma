import os
import discord
from PIL import Image


async def catlen(cmd, message, args):
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    length_number = int(str(target.id)[6]) + int(str(target.id)[9])
    img_height = 54
    img_width = 62 + (length_number * 15) + 50
    base = Image.new('RGBA', (img_width, img_height), (255, 255, 255, 0))
    image_location = 'meow'
    out_location = f'cache/meow_len_{message.id}.png'
    with Image.open(cmd.resource(f'{image_location}/bot.png')) as bot_cat_img:
        base.paste(bot_cat_img, (0, 0), bot_cat_img)
    with Image.open(cmd.resource(f'{image_location}/mid.png')) as mid_cat_img:
        for n in range(0, length_number - 1):
            base.paste(mid_cat_img, (62 + (n * 15), 0), mid_cat_img)
    with Image.open(cmd.resource(f'{image_location}/top.png')) as top_cat_img:
        base.paste(top_cat_img, (62 + ((length_number - 1) * 15), 0), top_cat_img)
    base.save(out_location)
    await message.channel.send(file=discord.File(out_location))
    os.remove(out_location)
