from requests import get as rg

from sigma.plugin import Plugin
from sigma.utils import create_logger

from config import WarGamingAppID


class WorldOfTanks(Plugin):
    is_global = True
    log = create_logger('wot')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'wot '):
            cmd_name = 'World of Warships'
            await self.client.send_typing(message.channel)
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            q = message.content[len(pfx) + len('wows') + 1:].lower()
            try:
                game_region, game_username = q.split(maxsplit=2)
            except:
                await self.client.send_message(message.channel, 'Insufficient parameters.')
                return
            regions_allowed = ['eu', 'na', 'asia', 'ru']
            if game_region not in regions_allowed:
                await self.client.send_message(message.channel,
                                               'Invalid region.\nThe bot only accepts `eu`, `na`, `ru` and `asia`')
                return
            if game_region == 'na':
                game_region = 'com'
            try:
                url_base = (
                'https://api.worldoftanks.' + game_region + '/wot/account/list/?application_id=' + WarGamingAppID + '&search=' + game_username)
                initial_data = rg(url_base).json()
            except:
                await self.client.send_message(message.channel, '`' + game_region + '` is not a valid region.')
                return
            try:
                if initial_data['status'].lower() == 'ok':
                    pass
                else:
                    return
            except Exception as err:
                print(err)
                return
            try:
                game_nickname = initial_data['data'][0]['nickname']
            except:
                await self.client.send_message(message.channel, 'User `' + game_username + '` not found.')
                return
            account_id = initial_data['data'][0]['account_id']
            url_second = 'https://api.worldofwarships.' + game_region + '/wows/account/info/?application_id=' + WarGamingAppID + '&account_id=' + str(account_id)
            main_data = rg(url_second).json()
            try:
                if main_data['status'].lower() == 'ok':
                    pass
                else:
                    return
            except Exception as err:
                print(err)
                return
            try:
                data = main_data['data'][str(account_id)]
                stats = data['statistics']['all']
                spotted = stats['spotted']
                max_xp = stats['max_xp']

                # Divider for clarity

                out_text = '```haskell'

                out_text += '\n```'

                # Divider for clarity

                await self.client.send_message(message.channel, out_text)
            except SyntaxError as err:
            #except Exception as err:
                print(err)
                await self.client.send_message(message.channel, 'We ran into an error, the user most likely doesn\'t exist in the region, or something dun goofed.\nError: **' + str(err) + '**')
                return
