
from steam import WebAPI

from sigma.plugin import Plugin
from sigma.utils import create_logger
from config import SteamAPI

class CSGO(Plugin):
    is_global = True
    log = create_logger('CSGO')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'csgo'):
            await self.client.send_typing(message.channel)
            cmd_name = 'CSGO'
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            try:
                csgo_input = message.content[len(pfx) + len('csgo') + 1:]
                api = WebAPI(SteamAPI)
                userID = api.ISteamUser.ResolveVanityURL(vanityurl=csgo_input, url_type=1)['response']['steamid']
                stats = api.ISteamUserStats.GetUserStatsForGame(steamid=userID, appid='730')['playerstats']['stats']
                summery = api.ISteamUser.GetPlayerSummaries(steamids=userID)['response']['players'][0]
                displayName = str(summery['personaname'])
                v='value'
                kills = stats[0][v]
                deaths =stats[1][v]
                KdR = kills/deaths
                playTime = str(stats[2][v])
                knifeKills=str(stats[9][v])
                headshotKills = str(stats[25][v])
                shotsFired=stats[47][v]
                shotsHit = stats[46][v]
                acc = shotsHit/shotsFired
                rounds=str(stats[48][v])
                mpv=str(stats[102][v])
                matchesWon = stats[127][v]
                matchesplayed= stats[128][v]
                matchesLost=matchesplayed - matchesWon
                winLoseRatio=matchesWon/matchesLost
                await self.client.send_message(message.channel, 'display name: ' + displayName +
                                                                '\nkills: '+str(kills)+
                                                                '\ndeaths: '+str(deaths)+
                                                                '\nKill Death Ratio: {:.2}'.format(KdR)+
                                                                '\ntime in game: '+playTime+'hours'+
                                                                '\nKnife Kills: '+knifeKills+
                                                                '\nHead Shot Kills: '+headshotKills+
                                                                '\nshots fired: '+str(shotsFired)+
                                                                '\nshots hit: '+str(shotsHit)+
                                                                '\naccuracy: {:.2}'.format(acc)+
                                                                '\nRounds Played: '+rounds+
                                                                '\ntimes MPV: '+mpv+
                                                                '\nMatches Won: '+str(matchesWon)+
                                                                '\nMatches Lost: '+str(matchesLost)+
                                                                '\nMatches Played: '+str(matchesplayed)+
                                                                '\nMatch Win/Lose ratio: {:.2}'.format(winLoseRatio))
            except:
                await self.client.send_message(message.channel, 'Something went wrong or the user was not found.')
