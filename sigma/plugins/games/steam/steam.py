from steam import WebAPI as steamwebapi
import time

from config import SteamAPI


async def steam(cmd, message, args):
    try:
        steamapi = steamwebapi(SteamAPI)
        steam_input = ' '.join(args)

        userID = steamapi.ISteamUser.ResolveVanityURL(vanityurl=steam_input, url_type=1)['response']['steamid']
        summery = steamapi.ISteamUser.GetPlayerSummaries(steamids=userID)['response']['players'][0]
        displayName = str(summery['personaname'])
        currentStamp = int(round(time.time()))
        creation = currentStamp - int(summery['timecreated'])
        lastOnline = currentStamp - int(summery['lastlogoff'])
        creation = int(creation) / 60 / 60 / 24 / 365.25
        lastOnline = time.strftime('%H:%M:%S', time.gmtime(int(lastOnline)))
        avatar = str(summery['avatarfull'])
        gameCount = str(steamapi.IPlayerService.GetOwnedGames(steamid=userID, include_appinfo=False, include_played_free_games=True, appids_filter=-1)['response']['game_count'])

        await cmd.reply(str('Display name : ' + str(displayName) + '\nTime on steam: ' + str(creation)[-1:] + ' years\nlast Online: ' + str(lastOnline) + ' ago\navatar: ' + str(avatar) + '\nnumber of games: ' + str(gameCount)))
    except Exception as e:
        cmd.log.error(e)
        await cmd.reply('an unknown error occured. is that your vanity URL?')
