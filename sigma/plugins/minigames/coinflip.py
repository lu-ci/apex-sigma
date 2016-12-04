import random
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import os

async def coinflip(cmd, message, args):
    cmd.db.add_stats('CoinFlipCount')
    cmd.db.add_points(message.server, message.author, 5)
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
        points = 10
        cost = 5
        choice = args[0]
        if choice.lower().startswith('t') or choice.lower().startswith('h'):
            cd_state = cmd.db.on_cooldown(message.server.id, message.author.id, 'CoinFlip', 20)
            if not cd_state:
                cmd.db.set_cooldown(message.server.id, message.author.id, 'CoinFlip')
            if choice.lower().startswith('t'):
                choice = 'tails'
            else:
                choice = 'heads'
            if result == choice.lower():
                out = 'Nice guess! :ballot_box_with_check:'
                if not cd_state:
                    cmd.db.add_points(message.server, message.author, points)
                    out += '\nYou\'ve been awarded **' + str(points) + '** points.'
                else:
                    out += '\nYou\'ve not been awarded cause the command is still on cooldown.'
            else:
                out = 'Better luck next time! :regional_indicator_x:'
                if not cd_state:
                    cmd.db.add_points(message.server, message.author, points)
                    out += '\nYou\'ve been charged **' + str(cost) + '** points.'
                else:
                    out += '\nYou\'ve not been charged cause the command is still on cooldown.'
            await cmd.bot.send_message(message.channel, out)
        else:
            await cmd.bot.send_message(message.channel, '**Heads** or **Tails** only, please.')
