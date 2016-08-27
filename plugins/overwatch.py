from plugin import Plugin
from commands import *
import urllib
import wget
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os

class Overwatch(Plugin):
    is_global = True

    async def on_message(self, message, pfx):

        # Overwatch API
        if message.content.startswith(pfx + cmd_overwatch + ' '):
            cmd_name = 'Overwatch'
            await self.client.send_typing(message.channel)
            ow_input = (str(message.content[len(cmd_overwatch) + 1 + len(pfx):])).replace('#', '-')
            ow_region_x, ignore, ow_name = ow_input.partition(' ')
            ow_region = ow_region_x.replace('NA', 'US')
            try:
                profile = ('http://127.0.0.1:9000/pc/' + ow_region.lower() + '/' + ow_name + '/profile').replace(' ', '')
                profile_json_source = urllib.request.urlopen(profile).read().decode('utf-8')
                profile_json = json.loads(profile_json_source)
                good = True
            except:
                await self.client.send_message(message.channel, 'Error 503: Service unavailable.')
                good = False
            if good:
                try:
                    avatar_link = profile_json['data']['avatar']
                    border_link = profile_json['data']['levelFrame']
                    wget.download(avatar_link)
                    avatar_link_base = 'https://blzgdapipro-a.akamaihd.net/game/unlocks/'
                    avatar_name = str(profile_json['data']['avatar'])
                    os.rename(avatar_name[len(avatar_link_base):], '/cache/ow/avatar_' + message.author.id + '.png')
                    wget.download(border_link)
                    border_link_base = 'https://blzgdapipro-a.akamaihd.net/game/playerlevelrewards/'
                    border_name = str(profile_json['data']['levelFrame'])
                    os.rename(border_name[len(border_link_base):], '/cache/ow/border_' + message.author.id + '.png')
                    base = Image.open('base.png')
                    overlay = Image.open('overlay.png')
                    foreground = Image.open('/cache/ow/border_' + message.author.id + 'avatar.png')
                    foreground_res = foreground.resize((128, 128), Image.ANTIALIAS)
                    background = Image.open('/cache/ow/avatar_' + message.author.id + 'avatar.png')
                    background_res = background.resize((72, 72), Image.ANTIALIAS)
                    base.paste(background_res, (28, 28))
                    base.paste(overlay, (0, 0), overlay)
                    base.paste(foreground_res, (0, 0), foreground_res)
                    base.save('profile.png')
                    if message.author.id == '152239976338161664':
                        rank_error = 'Goddamn it Bubu!'
                    else:
                        rank_error = 'Season not active.'
                    overwatch_profile = ('**Name:** ' + profile_json['data']['username'] +
                                         '\n**Level:** ' + str(profile_json['data']['level']) +
                                         '\n**Quick Games:**' +
                                         '\n    **- Played:** ' + str(profile_json['data']['games']['quick']['played']) +
                                         '\n    **- Won:** ' + str(profile_json['data']['games']['quick']['wins']) +
                                         '\n    **- Lost:** ' + str(profile_json['data']['games']['quick']['lost']) +
                                         '\n**Competitive Games:**' +
                                         '\n    **- Played:** ' + str(
                        profile_json['data']['games']['competitive']['played']) +
                                         '\n    **- Won:** ' + str(profile_json['data']['games']['competitive']['wins']) +
                                         '\n    **- Lost:** ' + str(profile_json['data']['games']['competitive']['lost']) +
                                         '\n    **- Rank:** ' + rank_error +
                                         '\n**Playtime:**' +
                                         '\n    **- Quick:** ' + str(profile_json['data']['playtime']['quick']) +
                                         '\n    **- Competitive:** ' + str(profile_json['data']['playtime']['competitive'])
                                         )
                    #print('CMD [' + cmd_name + '] > ' + initiator_data)
                    await self.client.send_file(message.channel, 'profile.png')
                    await self.client.send_message(message.channel, overwatch_profile)
                    if os.path.isfile('avatar.png'):
                        os.remove('avatar.png')
                    if os.path.isfile('border.png'):
                        os.remove('border.png')
                    if os.path.isfile('profile.png'):
                        os.remove('profile.png')
                except KeyError:
                    try:
                        #print('CMD [' + cmd_name + '] > ' + initiator_data)
                        print(profile_json['error'])
                        await self.client.send_message(message.channel, profile_json['error'])
                    except:
                        #print('CMD [' + cmd_name + '] > ' + initiator_data)
                        await self.client.send_message(message.channel,
                                                  'Something went wrong.\nThe servers are most likely overloaded, please try again.')
            #else:
                #print('CMD [' + cmd_name + '] > ' + initiator_data)