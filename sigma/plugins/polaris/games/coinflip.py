import random
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import os

async def coinflip(cmd, message, args):
    number = random.randint(0, 1)
    if number == 1:
        result = 'heads'
    else:
        result = 'tails'
    base = Image.open(cmd.resource('img/coin_base.png'))
    coin_image = Image.open(cmd.resource('img/' + result + '.png'))
    coin_overlay = Image.open(cmd.resource('img/coin_overlay.png'))
    base.paste(coin_image, (0, 0), coin_image)
    base.paste(coin_overlay, (0, 0), coin_overlay)
    font = ImageFont.truetype("big_noodle_titling_oblique.ttf", 80)
    imgdraw = ImageDraw.Draw(base)
    imgdraw.text((110, 8), result.title(), (255, 255, 255), font=font)
    base.save('cache/coin_' + message.author.id + '.png')
    await cmd.bot.send_file(message.channel, 'cache/coin_' + message.author.id + '.png')
    os.remove('cache/coin_' + message.author.id + '.png')
    if args:
        choice = args[0]
        if choice.lower().startswith('t') or choice.lower().startswith('h'):
            if result == choice.lower():
                await cmd.bot.send_message(message.channel, 'Nice guess! :ballot_box_with_check:')
            else:
                await cmd.bot.send_message(message.channel, 'Better luck next time! :regional_indicator_x:')
        else:
            await cmd.bot.send_message(message.channel, '**Heads** or **Tails** only, please.')
