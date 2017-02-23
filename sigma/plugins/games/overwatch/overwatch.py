import os
from io import BytesIO
import requests
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


# Overwatch API
async def overwatch(cmd, message, args):
    ow_input = (str(message.content[len('overwatch') + 1 + len(cmd.prefix):])).replace('#', '-')

    ow_region_x, ignore, ow_name = ow_input.partition(' ')
    ow_region = ow_region_x.lower().replace('na', 'us')

    if ow_region.upper() == 'NA' or 'US' or 'EU':
        try:
            profile = (
                'http://api.lootbox.eu/pc/' + ow_region.lower() + '/' + ow_name + '/profile').replace(' ', '')
            profile_json = requests.get(profile).json()
            champ_get_url = (
                'http://api.lootbox.eu/pc/' + ow_region.lower() + '/' + ow_name + '/quickplay/heroes').replace(' ', '')
            champ_get = requests.get(champ_get_url).json()
            avatar_link = profile_json['data']['avatar']
            border_link = profile_json['data']['levelFrame']
            if str(champ_get[0]['name']) == 'L&#xFA;cio':
                top_champ = 'Lucio'
            else:
                top_champ = str(champ_get[0]['name'])
            avatar = requests.get(avatar_link).content
            border = requests.get(border_link).content
            base = Image.open(cmd.resource('img/base.png'))
            overlay = Image.open(cmd.resource('img/overlay.png'))
            foreground = Image.open(BytesIO(border))
            foreground_res = foreground.resize((128, 128), Image.ANTIALIAS)
            background = Image.open(BytesIO(avatar))
            background_res = background.resize((72, 72), Image.ANTIALIAS)
            try:
                rank_link = profile_json['data']['competitive']['rank_img']
                rank = requests.get(rank_link).content
                rankimg = Image.open(BytesIO(rank))
                rankimg_res = rankimg.resize((64, 64), Image.ANTIALIAS)
            except:
                rankimg_res = None
            base.paste(background_res, (28, 28))
            base.paste(overlay, (0, 0), overlay)
            base.paste(foreground_res, (0, 0), foreground_res)
            try:
                base.paste(rankimg_res, (310, 32), rankimg_res)
            except:
                pass
            font = ImageFont.truetype("big_noodle_titling_oblique.ttf", 32)
            font2 = ImageFont.truetype("big_noodle_titling_oblique.ttf", 16)
            imgdraw = ImageDraw.Draw(base)
            imgdraw.text((130, 38), profile_json['data']['username'], (255, 255, 255), font=font)
            imgdraw.text((130, 70), 'Most Played: ' + top_champ, (255, 255, 255), font=font2)
            base.save('cache/ow_profile_' + message.author.id + '.png')
            name = profile_json['data']['username']
            level = str(profile_json['data']['level'])
            qg_won = str(profile_json['data']['games']['quick']['wins'])
            qg_playtime = str(profile_json['data']['playtime']['quick'])
            try:
                cg_played = str(profile_json['data']['games']['competitive']['played'])
            except:
                cg_played = 'None'
            try:
                cg_won = str(profile_json['data']['games']['competitive']['wins'])
            except:
                cg_won = 'None'
            try:
                cg_lost = str(profile_json['data']['games']['competitive']['lost'])
            except:
                cg_lost = 'None'
            try:
                rank = str(profile_json['data']['competitive']['rank'])
            except:
                rank = 'None'
            try:
                cg_playtime = str(profile_json['data']['playtime']['competitive'])
            except:
                cg_playtime = 'None'
            overwatch_profile = ('```Name: ' + name +
                                 '\nLevel: ' + level +
                                 '\nQuick Games:' +
                                 '\n    - Won: ' + qg_won +
                                 '\nCompetitive Games:' +
                                 '\n    - Played: ' + cg_played +
                                 '\n    - Won: ' + cg_won +
                                 '\n    - Lost: ' + cg_lost +
                                 '\n    - Rank: ' + rank +
                                 '\nPlaytime:' +
                                 '\n    - Quick: ' + qg_playtime +
                                 '\n    - Competitive: ' + cg_playtime + '```')
            # print('CMD [' + cmd_name + '] > ' + initiator_data)
            await cmd.bot.send_file(message.channel, 'cache/ow_profile_' + message.author.id + '.png')
            os.remove('cache/ow_profile_' + message.author.id + '.png')
            await cmd.bot.send_message(message.channel, overwatch_profile)
        except KeyError:
            try:
                # print('CMD [' + cmd_name + '] > ' + initiator_data)
                print(profile_json['error'])
                await cmd.bot.send_message(message.channel, profile_json['error'])
            except:
                # print('CMD [' + cmd_name + '] > ' + initiator_data)
                await cmd.bot.send_message(message.channel,
                                           'Something went wrong.\nThe servers are most likely overloaded, please try again.')
                # else:
                # print('CMD [' + cmd_name + '] > ' + initiator_data)
    else:
        await cmd.bot.send_message(message.channel,
                                   'Invalid region: `' + ow_region.upper() + '`\nAccepted regions are `NA`, `US` and `EU`\nUsage: `' + cmd.prefix + 'overwatch' + 'region battletag#ID')
