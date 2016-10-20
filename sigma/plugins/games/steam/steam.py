from steam import WebAPI as steamwebapi
import time

from config import SteamAPI


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
            await cmd.reply('User Not Found...')
            return
        gamecount_call = steamapi.call('IPlayerService.GetOwnedGames', steamid=userid, include_appinfo=False, include_played_free_games=True, appids_filter=-1)
        gamecountnonfree_call = steamapi.call('IPlayerService.GetOwnedGames', steamid=userid, include_appinfo=False, include_played_free_games=False, appids_filter=-1)
        print(response)
        print(userid)
        summary_call = steamapi.call('ISteamUser.GetPlayerSummaries', steamids=userid)
        summary = summary_call['response']['players'][0]
        print(summary)
        displayname = str(summary['personaname'])
        currentstamp = int(round(time.time()))
        creation = currentstamp - int(summary['timecreated'])
        lastonline = currentstamp - int(summary['lastlogoff'])
        creation = int(creation) / 60 / 60 / 24 / 365.25
        lastonline = time.strftime('%H:%M:%S', time.gmtime(int(lastonline)))
        onlinenow = summary['personastate']
        avatar = str(summary['avatarfull'])
        gamecount = gamecount_call['response']['game_count']
        gamecountnonfree = gamecountnonfree_call['response']['game_count']
        # Data Collection End, Pillow Start

    except SyntaxError as e:
        await cmd.reply('An unknown error occurred. is that your vanity URL?')
        print(e)
