from steam import WebAPI as steamwebapi
from config import SteamAPI
from io import BytesIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import time
import requests
import os


async def steam(cmd, message, args):
    try:
        steamapi = steamwebapi(SteamAPI)

        steam_input = ' '.join(args)
        # Data Collection Start
        response_call = steamapi.call('ISteamUser.ResolveVanityURL', vanityurl=str(steam_input), url_type=1)
        try:
            response = response_call['response']
            userid = response['steamid']
        except Exception as e:
            await cmd.reply('User Not Found Or Profile Private...')
            return
        gamecount_call = steamapi.call('IPlayerService.GetOwnedGames', steamid=userid, include_appinfo=False,
                                       include_played_free_games=True, appids_filter=-1)
        gamecountnonfree_call = steamapi.call('IPlayerService.GetOwnedGames', steamid=userid, include_appinfo=False,
                                              include_played_free_games=False, appids_filter=-1)
        summary_call = steamapi.call('ISteamUser.GetPlayerSummaries', steamids=userid)
        summary = summary_call['response']['players'][0]
        displayname = str(summary['personaname'])
        currentstamp = int(round(time.time()))
        creation = currentstamp - int(summary['timecreated'])
        lastonline = currentstamp - int(summary['lastlogoff'])
        creation = int(creation) / 60 / 60 / 24 / 365.25
        lastonline = time.strftime('%H:%M:%S', time.gmtime(int(lastonline)))
        onlinenow = summary['personastate']
        avatar_url = str(summary['avatarfull'])
        gamecount = gamecount_call['response']['game_count']
        gamecountnonfree = gamecount - gamecountnonfree_call['response']['game_count']
        # Data Collection End, Pillow Start
        avatar_raw = requests.get(avatar_url).content

        with Image.open(BytesIO(avatar_raw)) as avatar:
            base = Image.open(cmd.resource('img/base.png'))
            overlay = Image.open(cmd.resource('img/overlay.png'))
            base.paste(avatar, (0, 0))
            base.paste(overlay, (0, 0), overlay)
            font = ImageFont.truetype("big_noodle_titling_oblique.ttf", 40)
            font2 = ImageFont.truetype("big_noodle_titling_oblique.ttf", 30)
            imgdraw = ImageDraw.Draw(base)
            imgdraw.text((190, 7), displayname, (255, 255, 255), font=font)
            imgdraw.text((190, 45), 'Member for ' + str(creation)[-1:] + ' years', (255, 255, 255), font=font2)
            imgdraw.text((190, 75), 'Last Logoff: ' + str(lastonline) + ' ago', (255, 255, 255), font=font2)
            imgdraw.text((190, 105), 'Has ' + str(gamecount) + ' games', (255, 255, 255), font=font2)
            imgdraw.text((190, 135), 'Out of which ' + str(gamecountnonfree) + ' are free', (255, 255, 255), font=font2)
            if onlinenow == 0:
                imgdraw.text((2, 165), '*', (102, 102, 153), font=font)
            elif onlinenow == 1:
                imgdraw.text((2, 165), '*', (26, 188, 156), font=font)
            elif onlinenow == 2:
                imgdraw.text((2, 165), '*', (255, 51, 0), font=font)
            elif onlinenow == 3:
                imgdraw.text((2, 165), '*', (255, 153, 0), font=font)
            else:
                imgdraw.text((2, 165), '*', (102, 102, 153), font=font)
            base.save('cache/steam_' + message.author.id + '.png')
        await cmd.reply_file('cache/steam_' + message.author.id + '.png')
        os.remove('cache/steam_' + message.author.id + '.png')
    except Exception as e:
        cmd.log.error(e)
        await cmd.reply('An unknown error occurred.\nError: ' + str(e))
