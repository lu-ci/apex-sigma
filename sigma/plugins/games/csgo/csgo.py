from steam import WebAPI

from config import SteamAPI


async def csgo(cmd, message, args):
    csgo_input = ' '.join(args)

    try:
        api = WebAPI(SteamAPI)
        userID = api.call('ISteamUser.ResolveVanityURL', vanityurl=csgo_input, url_type=1)['response']['steamid']
        stats = api.call('ISteamUserStats.GetUserStatsForGame', steamid=userID, appid='730')['playerstats']['stats']
        summery = api.call('ISteamUser.GetPlayerSummaries', steamids=userID)['response']['players'][0]

        displayName = str(summery['personaname'])
        v = 'value'
        kills = stats[0][v]
        deaths = stats[1][v]
        KdR = kills / deaths
        playTime = str(stats[2][v])
        knifeKills = str(stats[9][v])
        headshotKills = str(stats[25][v])
        shotsFired = stats[47][v]
        shotsHit = stats[46][v]
        acc = shotsHit / shotsFired
        rounds = str(stats[48][v])
        mpv = str(stats[102][v])
        matchesWon = stats[127][v]
        matchesplayed = stats[128][v]
        matchesLost = matchesplayed - matchesWon
        winLoseRatio = matchesWon / matchesLost

        await cmd.bot.send_message(message.channel, 'Display name: ' + displayName +
                        '\nKills: ' + str(kills) +
                        '\nDeaths: ' + str(deaths) +
                        '\nKill Death Ratio: {:.2}'.format(KdR) +
                        '\nDime in game: ' + playTime + 'hours' +
                        '\nKnife Kills: ' + knifeKills +
                        '\nHead Shot Kills: ' + headshotKills +
                        '\nShots fired: ' + str(shotsFired) +
                        '\nShots hit: ' + str(shotsHit) +
                        '\nAccuracy: {:.2}'.format(acc) +
                        '\nRounds Played: ' + rounds +
                        '\nTimes MPV: ' + mpv +
                        '\nMatches Won: ' + str(matchesWon) +
                        '\nMatches Lost: ' + str(matchesLost) +
                        '\nMatches Played: ' + str(matchesplayed) +
                        '\nMatch Win/Lose ratio: {:.2}'.format(winLoseRatio))
    except Exception as e:
        cmd.log.error(e)
        await cmd.bot.send_message(message.channel, 'Something went wrong or the user was not found.')
