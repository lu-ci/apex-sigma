from PIL import Image
from sigma.core.utils import user_avatar
import os
import imageio
import discord
import aiohttp
import random
from io import BytesIO


async def triggered(cmd, message, args):
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    if not cmd.cooldown.on_cooldown(cmd, message):
        cmd.cooldown.set_cooldown(cmd, message, 180)
        avatar_url = user_avatar(target) + '?size=512'
        wait_trig_response = discord.Embed(color=0xff6600, title='💥 Triggering...')
        resp_msg = await message.channel.send(embed=wait_trig_response)
        async with aiohttp.ClientSession() as session:
            async with session.get(avatar_url) as data:
                avatar_data = await data.read()
                avatar = Image.open(BytesIO(avatar_data))
                avatar = avatar.resize((300, 300), Image.ANTIALIAS)
        image_list = []
        for x in range(0, 30):
            base = Image.new('RGBA', (256, 320), (0, 0, 0, 0))
            with Image.open(cmd.resource('trig_bot.png')) as trig_sign:
                move_max = 22
                move_x = random.randint(-move_max, move_max)
                move_y = random.randint(-move_max, move_max)
                base.paste(avatar, (-22 + move_x, -22 + move_y))
                base.paste(trig_sign, (0, 256))
                temp_loc = f'temp_gif_cache_{random.randint(99, 999999)}.png'
                base.save(temp_loc)
                image_list.append(imageio.imread(temp_loc))
                os.remove(temp_loc)
        out_loc = f'cache/triggered_{message.id}.gif'
        imageio.mimsave(out_loc, image_list, fps=30)
        dfile = discord.File(out_loc)
        await message.channel.send(file=dfile)
        try:
            await resp_msg.delete()
        except:
            pass
        os.remove(out_loc)
    else:
        cdembed = discord.Embed(color=0x696969, title=f'🕙 {target.name} has been put on ice to cool off.')
        await message.channel.send(embed=cdembed)

