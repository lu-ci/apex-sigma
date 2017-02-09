import requests
from PIL import Image
from io import BytesIO
import os


async def dog(cmd, message, args):
    doggie_url = 'http://www.randomdoggiegenerator.com/randomdoggie.php'
    doggie_image = requests.get(doggie_url).content
    with Image.open(BytesIO(doggie_image)) as img:
        img.save('cache/pupper_' + message.id + '.png')
    await cmd.bot.send_file(message.channel, 'cache/pupper_' + message.id + '.png')
    os.remove('cache/pupper_' + message.id + '.png')
