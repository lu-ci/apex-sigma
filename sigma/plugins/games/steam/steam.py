from steam import WebAPI as steamwebapi
import time

from config import SteamAPI


async def steam(cmd, message, args):
    try:
        steamapi = steamwebapi(SteamAPI)
        steam_input = ' '.join(args)

        userID = steamapi.ISteamUser.ResolveVanityURL(vanityurl=steam_input, url_type=1)['response']['steamid']
        summary = steamapi.ISteamUser.GetPlayerSummaries(steamids=userID)['response']['players'][0]

        displayName = summary['personaname']
        currentStamp = int(round(time.time()))
        lastOnline = currentStamp - int(summary['lastlogoff'])
        lastOnline = time.strftime('%H:%M:%S', time.gmtime(lastOnline))
        creation = currentStamp - int(summary['timecreated'])
        creation = creation / 60 / 60 / 24 / 365.25

        avatar = str(summary['avatarfull'])

        gameCount = steamapi.IPlayerService.GetOwnedGames(steamid=userID, include_appinfo=False, include_played_free_games=True, appids_filter=-1)['response']['game_count']
        gameCountNonFree = steamapi.IPlayerService.GetOwnedGames(steamid=userID, include_appinfo=False, include_played_free_games=False, appids_filter=-1)['response']['game_count']

        msg = 'Display name: {:s}\n'
        msg += 'Time on steam: {:s} years\n'
        msg += 'last Online: {:s} ago\n'
        msg += 'avatar: {:s}\n'
        msg += 'number of games: {:d}, of wich {:d} are free.'
        await cmd.reply(msg.format(displayName, str(creation)[-1:], lastOnline,
                        avatar, gameCount, gameCount - gameCountNonFree))
    except Exception as e:
        cmd.log.error(e)
        await cmd.reply('an unknown error occured. is that your vanity URL?')
