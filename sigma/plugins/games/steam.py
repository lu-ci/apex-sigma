from steam import WebAPI as steam
import time

from sigma.plugin import Plugin
from sigma.utils import create_logger

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
                displayName = str(summery['personaname'])
                currentStamp = int(round(time.time()))
                creation = currentStamp - int(summery['timecreated'])
                lastOnline = currentStamp - int(summery['lastlogoff'])
                creation = int(creation) / 60 /60 / 24 / 365.25
                lastOnline = time.strftime('%H:%M:%S', time.gmtime(int(lastOnline)))
                avatar = str(summery['avatarfull'])
                gameCount = steamapi.IPlayerService.GetOwnedGames(steamid=userID, include_appinfo=False, include_played_free_games=True,appids_filter=-1)['response']['game_count']
                gameCountNonFree = steamapi.IPlayerService.GetOwnedGames(steamid=userID, include_appinfo=False, include_played_free_games=False,appids_filter=-1)['response']['game_count']
                await self.client.send_message(message.channel, str('Display name : '+ displayName+ '\nTime on steam: '+str(creation)[-1:]+' years\nlast Online: '+ str(lastOnline)+' ago\navatar: '+avatar+'\nnumber of games: ' +str(gameCount)+', of which '+str(gameCount - gameCountNonFree) +' are free.'))
            except:
                await self.client.send_message(message.channel, 'an unknown error ocoured. is that your vanity URL?')
