from plugin import Plugin
from config import cmd_overwatch
import urllib.request
import wget
import os
import requests
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import json
from utils import create_logger


class Overwatch(Plugin):
    is_global = True
    log = create_logger(cmd_overwatch)

    async def on_message(self, message, pfx):

        # Overwatch API
        if message.content.startswith(pfx + cmd_overwatch + ' '):
            cmd_name = 'Overwatch'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            await self.client.send_typing(message.channel)
            ow_input = (str(message.content[len(cmd_overwatch) + 1 + len(pfx):])).replace('#', '-')
            ow_region_x, ignore, ow_name = ow_input.partition(' ')
            ow_region = ow_region_x.replace('NA', 'US')
            if os.path.isfile('cache/ow/avatar_' + message.author.id + '.png'):
                os.remove('cache/ow/avatar_' + message.author.id + '.png')
            if os.path.isfile('cache/ow/border_' + message.author.id + '.png'):
                os.remove('cache/ow/border_' + message.author.id + '.png')
            if os.path.isfile('cache/ow/profile_' + message.author.id + '.png'):
                os.remove('cache/ow/profile_' + message.author.id + '.png')
            if os.path.isfile('cache/ow/rank_' + message.author.id + '.png'):
                os.remove('cache/ow/rank_' + message.author.id + '.png')
            if ow_region.upper() == 'NA' or 'US' or 'EU':
                try:
                    profile = (
                        'http://127.0.0.1:9000/pc/' + ow_region.lower() + '/' + ow_name + '/profile').replace(' ', '')
                    profile_json_source = urllib.request.urlopen(profile).read().decode('utf-8')
                    profile_json = json.loads(profile_json_source)
                    champ_get_url = (
                        'http://127.0.0.1:9000/pc/' + ow_region.lower() + '/' + ow_name + '/quick-play/heroes').replace(' ', '')
                    champ_get_src = urllib.request.urlopen(champ_get_url).read().decode('utf-8')
                    champ_get = json.loads(champ_get_src)
                    avatar_link = profile_json['data']['avatar']
                    border_link = profile_json['data']['levelFrame']
                    if str(champ_get[0]['name']) == 'L&#xFA;cio':
                        top_champ = 'Lucio'
                    else:
                        top_champ = str(champ_get[0]['name'])
                    avaloc = 'cache/ow/avatar_' + message.author.id + '.png'
                    borloc = 'cache/ow/border_' + message.author.id + '.png'
                    wget.download(avatar_link, out=avaloc)
                    # avatar_link_base = 'https://blzgdapipro-a.akamaihd.net/game/unlocks/'
                    # avatar_name = str(profile_json['data']['avatar'])
                    # os.rename(avatar_name[len(avatar_link_base):], '/cache/ow/avatar_' + message.author.id + '.png')
                    wget.download(border_link, out=borloc)
                    # border_link_base = 'https://blzgdapipro-a.akamaihd.net/game/playerlevelrewards/'
                    # border_name = str(profile_json['data']['levelFrame'])
                    # os.rename(border_name[len(border_link_base):], '/cache/ow/border_' + message.author.id + '.png')
                    base = Image.open('img/ow/base.png')
                    overlay = Image.open('img/ow/overlay.png')
                    foreground = Image.open('cache/ow/border_' + message.author.id + '.png')
                    foreground_res = foreground.resize((128, 128), Image.ANTIALIAS)
                    background = Image.open('cache/ow/avatar_' + message.author.id + '.png')
                    background_res = background.resize((72, 72), Image.ANTIALIAS)
                    try:
                        rank_link = profile_json['data']['competitive']['rank_img']
                        rankloc = 'cache/ow/rank_' + message.author.id + '.png'
                        wget.download(rank_link, out=rankloc)
                        rankimg = Image.open('cache/ow/rank_' + message.author.id + '.png')
                        rankimg_res = rankimg.resize((64, 64), Image.ANTIALIAS)
                    except:
                        pass
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
                    base.save('cache\ow\profile_' + message.author.id + '.png')
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
                    await self.client.send_file(message.channel, 'cache\ow\profile_' + message.author.id + '.png')
                    await self.client.send_message(message.channel, overwatch_profile)
                except KeyError:
                    try:
                        # print('CMD [' + cmd_name + '] > ' + initiator_data)
                        print(profile_json['error'])
                        await self.client.send_message(message.channel, profile_json['error'])
                    except:
                        # print('CMD [' + cmd_name + '] > ' + initiator_data)
                        await self.client.send_message(message.channel,
                                                       'Something went wrong.\nThe servers are most likely overloaded, please try again.')
                        # else:
                        # print('CMD [' + cmd_name + '] > ' + initiator_data)
            else:
                await self.client.send_message(message.channel,
                                               'Invalid region: `' + ow_region.upper() + '`\nAccepted regions are `NA`, `US` and `EU`\nUsage: `' + pfx + cmd_overwatch + 'region battletag#ID')
