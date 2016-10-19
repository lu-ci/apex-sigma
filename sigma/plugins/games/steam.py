from steam import WebAPI as steam
import time

from sigma.plugin import Plugin
from sigma.utils import create_logger, elapsedtime

from config import SteamAPI

class Steam(Plugin):
    is_global = True
    log = create_logger('steam')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx+'steam'):
            await self.client.send_typing(message.channel)
            cmd_name = 'Steam'
            try:
                self.log.info('User %s [%s] on server %s [%s] used the '+ cmd_name + ' command on #%s channel',
                message.author,
                message.author.id,
                message.server.name,
                message.server.id,
                message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                        message.author,
                        message.author.id)

            try:
                steamapi = steam(SteamAPI)
                steam_input = message.content[len(pfx)+len('steam')+1:]
                userID = steamapi.ISteamUser.ResolveVanityURL(vanityurl=steam_input, url_type=1)['response']['steamid']
                summery = steamapi.ISteamUser.GetPlayerSummaries(steamids=userID)['response']['players'][0]
                print(type(summery))
                displayName = str(summery['personaname'])
                currentStamp = int(round(time.time()))
                creation = currentStamp - int(summery['timecreated'])
                lastOnline = currentStamp - int(summery['lastlogoff'])
                creation = elapsedtime(creation)
                lastOnline=elapsedtime(lastOnline)
                avatar = str(summery['avatarfull'])
                gameCount = str(steamapi.IPlayerService.GetOwnedGames(steamid=userID, include_appinfo=False, include_played_free_games=True,appids_filter=-1)['response']['game_count'])
                await self.client.send_message(message.channel, str('Display name : '+ str(displayName)+ '\ntime on steam: '+str(creation)+'\nlast Online: '+ str(lastOnline)+'\navatar: '+str(avatar)+'\nnumber of games: ' +str(gameCount)))
            except:
                await self.client.send_message(message.channel, 'an unknown error ocoured. is that your vanity URL?')
