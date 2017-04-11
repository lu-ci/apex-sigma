from steam import WebAPI as steamwebapi
from config import SteamAPI
from io import BytesIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import time
import aiohttp
import os
import datetime
import discord


async def steam(cmd, message, args):
    steamapi = steamwebapi(SteamAPI)
    steam_input = ' '.join(args)
    # Data Collection Start
    response_call = steamapi.call('ISteamUser.ResolveVanityURL', vanityurl=str(steam_input), url_type=1)
    try:
        response = response_call['response']
        userid = response['steamid']
    except Exception as e:
        await message.channel.send('User Not Found Or Profile Private...')
        return
    gamecount_call = steamapi.call('IPlayerService.GetOwnedGames', steamid=userid, include_appinfo=False,
                                   include_played_free_games=True, appids_filter=-1)
    gamecountnonfree_call = steamapi.call('IPlayerService.GetOwnedGames', steamid=userid, include_appinfo=False,
                                          include_played_free_games=False, appids_filter=-1)
    summary_call = steamapi.call('ISteamUser.GetPlayerSummaries', steamids=userid)
    summary = summary_call['response']['players'][0]
    displayname = str(summary['personaname'])
    currentstamp = int(round(time.time()))
    creation = summary['timecreated']
    lastonline = currentstamp - int(summary['lastlogoff'])
    fmt = '%B %d, %Y'
    creation = datetime.datetime.fromtimestamp(creation).strftime(fmt)
    lastonline = time.strftime('%H:%M:%S', time.gmtime(int(lastonline)))
    onlinenow = summary['personastate']
    avatar_url = str(summary['avatarfull'])
    gamecount = gamecount_call['response']['game_count']
    gamecountnonfree = gamecount - gamecountnonfree_call['response']['game_count']
    # Data Collection End, Pillow Start
    async with aiohttp.ClientSession() as session:
        async with session.get(avatar_url) as data:
            avatar_raw = await data.read()
    with Image.open(BytesIO(avatar_raw)) as avatar:
        base = Image.open(cmd.resource('img/base.png'))
        overlay = Image.open(cmd.resource('img/overlay.png'))
        base.paste(avatar, (0, 0))
        base.paste(overlay, (0, 0), overlay)
        main_font = cmd.resource('fonts/NotoSansCJKjp-Medium.otf')
        font = ImageFont.truetype(main_font, 32)
        font2 = ImageFont.truetype(main_font, 23)
        imgdraw = ImageDraw.Draw(base)
        if len(displayname) > 18:
            displayname = displayname[:17] + '...'
        imgdraw.text((190, 7), displayname, (255, 255, 255), font=font)
        imgdraw.text((190, 45), 'Joined ' + str(creation), (255, 255, 255), font=font2)
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
        base.save(f'cache/steam_{message.id}.png')
    await message.channel.send(file=discord.File(f'cache/steam_{message.id}.png'))
    os.remove(f'cache/steam_{message.id}.png')
