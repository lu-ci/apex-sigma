import os
import requests
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw

from config import RLAPIKey


async def rl(cmd, message, args):
    rl_input = ' '.join(args).lower()

    try:
        platform, user = rl_input.split(maxsplit=1)
    except:
        await cmd.bot.send_message(message.channel, 'Wrong input format!')
        return

    if platform.lower() == 'steam':
        platform = '1'
    elif platform.lower() == 'playstation' or platform.lower() == 'psn' or platform.lower() == 'ps':
        platform = '2'
    elif platform.lower() == 'xbox':
        platform = '3'
    else:
        await cmd.bot.send_message(message.channel, 'Platform unrecognized.')
        return

    url_base = 'http://rltracker.pro/api/profile/get?api_key=' + RLAPIKey + '&platform=' + platform + '&id=' + user
    rl_data = requests.get(url_base).json()

    try:
        nick = rl_data['player']['nickname']
        avatar = rl_data['player']['avatar']

        solo_rn = rl_data['ranking']['10']
        solo_rn_rank = solo_rn['rating']
        solo_rn_tier = solo_rn['tier_id']

        doubles_rn = rl_data['ranking']['11']
        doubles_rn_rank = doubles_rn['rating']
        doubles_rn_tier = doubles_rn['tier_id']

        solo_str_rn = rl_data['ranking']['12']
        solo_str_rn_rank = solo_str_rn['rating']
        solo_str_rn_tier = solo_str_rn['tier_id']

        str_rn = rl_data['ranking']['13']
        str_rn_rank = str_rn['rating']
        str_rn_tier = str_rn['tier_id']

        wins = rl_data['stats']['wins']
        goals = rl_data['stats']['goals']
        mvps = rl_data['stats']['mpvs']
        saves = rl_data['stats']['saves']
        shots = rl_data['stats']['shots']
        assists = rl_data['stats']['assists']

        profile_url = rl_data['url']

        solo_tier_img = cmd.resource('img/ranks/' + str(solo_rn_tier) + '.png')
        doubles_tier_img = cmd.resource('img/ranks/' + str(doubles_rn_tier) + '.png')
        solo_str_tier_img = cmd.resource('img/ranks/' + str(solo_str_rn_tier) + '.png')
        str_tier_img = cmd.resource('img/ranks/' + str(str_rn_tier) + '.png')

        solo_img = Image.open(solo_tier_img)
        doubles_img = Image.open(doubles_tier_img)
        solo_str_img = Image.open(solo_str_tier_img)
        str_img = Image.open(str_tier_img)

        avatar_raw = requests.get(avatar).content
        avatar_img_raw_res = Image.open(BytesIO(avatar_raw))
        avatar_img = avatar_img_raw_res.resize((42, 42), Image.ANTIALIAS)

        solo_img_res = solo_img.resize((40, 40), Image.ANTIALIAS)
        doubles_img_res = doubles_img.resize((40, 40), Image.ANTIALIAS)
        solo_str_img_res = solo_str_img.resize((40, 40), Image.ANTIALIAS)
        str_img_res = str_img.resize((40, 40), Image.ANTIALIAS)

        base = Image.open(cmd.resource('img/base_rl.png'))
        overlay = Image.open(cmd.resource('img/overlay.png'))
        base.paste(avatar_img, (369, 3))
        base.paste(overlay, (0, 0), overlay)

        base.paste(solo_img_res, (224, 81), solo_img_res)
        base.paste(doubles_img_res, (349, 81), doubles_img_res)
        base.paste(solo_str_img_res, (224, 147), solo_str_img_res)
        base.paste(str_img_res, (349, 147), str_img_res)

        font1 = ImageFont.truetype("big_noodle_titling_oblique.ttf", 35)
        font2 = ImageFont.truetype("big_noodle_titling_oblique.ttf", 30)
        font3 = ImageFont.truetype("big_noodle_titling_oblique.ttf", 26)

        imgdraw = ImageDraw.Draw(base)
        imgdraw.text((5, 5), nick, (255, 255, 255), font=font1)

        imgdraw.text((50, 62), str(wins), (255, 255, 255), font=font2)
        imgdraw.text((50, 110), str(goals), (255, 255, 255), font=font2)
        imgdraw.text((50, 157), str(mvps), (255, 255, 255), font=font2)
        imgdraw.text((163, 62), str(saves), (255, 255, 255), font=font2)
        imgdraw.text((163, 110), str(shots), (255, 255, 255), font=font2)
        imgdraw.text((163, 157), str(assists), (255, 255, 255), font=font2)

        imgdraw.text((269, 80), str(solo_rn_rank), (255, 255, 255), font=font3)
        imgdraw.text((269, 146), str(solo_str_rn_rank), (255, 255, 255), font=font3)
        imgdraw.text((394, 80), str(doubles_rn_rank), (255, 255, 255), font=font3)
        imgdraw.text((394, 146), str(str_rn_rank), (255, 255, 255), font=font3)

        base.save('cache/rl_' + message.author.id + '.png')
        await cmd.bot.send_file(message.channel, message.channel, 'cache/rl_' + message.author.id + '.png')
        await cmd.bot.send_message(message.channel, 'You can find more at:\n<' + profile_url + '>')
        os.remove('cache/rl_' + message.author.id + '.png')
    except Exception:
        try:
            error = rl_data['error']
            await cmd.bot.send_message(message.channel, 'Error: ' + str(error))
        except Exception:
            await cmd.bot.send_message(message.channel, 'Could not retrieve webpage.\nUser not found or the service goofed.')
