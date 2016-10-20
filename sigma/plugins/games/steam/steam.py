from steam import WebAPI as steamwebapi
import time

from config import SteamAPI


async def steam(cmd, message, args):
    try:
        steamapi = steamwebapi(SteamAPI)
        steam_input = ' '.join(args)
        userID = steamapi.ISteamUser.ResolveVanityURL(vanityurl=steam_input, url_type=1)['response']['steamid']
        summary = steamapi.ISteamUser.GetPlayerSummaries(steamids=userID)['response']['players'][0]
        displayName = str(summary['personaname'])
        currentStamp = int(round(time.time()))
        creation = currentStamp - int(summary['timecreated'])
        lastOnline = currentStamp - int(summary['lastlogoff'])
        creation = int(creation) / 60 / 60 / 24 / 365.25
        lastOnline = time.strftime('%H:%M:%S', time.gmtime(int(lastOnline)))
        onlineNow = summary['personastate']
        if (onlineNow):
            try:
                currentGame = summary['gameextrainfo']
            except:
                currentGame = 'None'
        avatar = str(summary['avatarfull'])
        gameCount = \
            steamapi.IPlayerService.GetOwnedGames(steamid=userID, include_appinfo=False, include_played_free_games=True,
                                                  appids_filter=-1)['response']['game_count']
        gameCountNonFree = steamapi.IPlayerService.GetOwnedGames(steamid=userID, include_appinfo=False,
                                                                 include_played_free_games=False, appids_filter=-1)[
            'response']['game_count']
        if (onlineNow):
            await cmd.reply(str('Display name : ' + displayName +
                                '\nTime on steam: ' + str(creation)[
                                                      -1:] + ' years' +
                                '\nThis User is Currently Online' +
                                '\navatar: ' + avatar +
                                '\nnumber of games: ' + str(
                gameCount) + ', of which ' + str(gameCount - gameCountNonFree) + ' are free.'))
        else:
            await cmd.reply(str('Display name : ' + displayName +
                                '\nTime on steam: ' + str(creation)[
                                                      -1:] + ' years' +
                                '\nlast Online: ' + str(lastOnline) + ' ago' +
                                '\navatar: ' + avatar +
                                '\nnumber of games: ' + str(
                gameCount) + ', of which ' + str(gameCount - gameCountNonFree) + ' are free.'))

    except SyntaxError as e:
        await cmd.reply('An unknown error ocoured. is that your vanity URL?')
        print(e)
