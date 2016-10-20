import os
import requests
from io import BytesIO
from PIL import Image


async def osu(cmd, message, args):
    try:
        osu_input = ' '.join(args)

        sig_url = 'https://lemmmy.pw/osusig/sig.php?colour=pink&uname=' + osu_input
        sig = requests.get(sig_url).content
        sig_img = Image.open(BytesIO(sig))

        sig_img.save('cache/img_' + message.author.id + '.png')
        await cmd.reply_file('cache/img_' + message.author.id + '.png')
        os.remove('cache/img_' + message.author.id + '.png')
    except Exception as e:
        cmd.log.error(e)
        await cmd.reply('Something went wrong or the user was not found.')
