from plugin import Plugin
from utils import create_logger
from config import WarGamingAppID
from requests import get as rg
import datetime

class WorlfOfWarships(Plugin):

    is_global = True
    log = create_logger('wows')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'wows '):
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
            game_region, game_username = q.split(maxsplit=1)
            if game_region == 'na':
                game_region = 'com'
            try:
                url_base = 'https://api.worldofwarships.' + game_region + '/wows/account/list/?application_id=' + WarGamingAppID + '&search=' + game_username
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
                last_battle = data['last_battle_time']
                last_battle_conv = datetime.datetime.fromtimestamp(last_battle).strftime('%B %d, %Y %H:%M')
                leveling_tier = data['leveling_tier']
                join_date = data['created_at']
                join_date_conv = datetime.datetime.fromtimestamp(join_date).strftime('%B %d, %Y %H:%M')

                stats = data['statistics']
                distance = stats['distance']
                battle_count = stats['battles']

                pvp_stats = stats['pvp']
                max_xp = pvp_stats['max_xp']
                max_spotted_dmg = pvp_stats['max_damage_scouting']

                main_battery = pvp_stats['main_battery']
                max_frags = main_battery['max_frags_battle']
                frags = main_battery['frags']
                hits = main_battery['hits']
                max_frags_ship_id = main_battery['max_frags_ship_id']
                shots = main_battery['shots']

                max_frags_ship_url = 'https://api.worldofwarships.' + game_region + '/wows/encyclopedia/ships/?application_id=' + WarGamingAppID + '&ship_id=' + str(max_frags_ship_id)
                max_frags_ship_data = rg(max_frags_ship_url).json()

                if max_frags_ship_id is not None:
                    max_frags_ship_name = max_frags_ship_data['data'][str(max_frags_ship_id)]['name']
                    max_frags_ship_tier = max_frags_ship_data['data'][str(max_frags_ship_id)]['tier']
                else:
                    max_frags_ship_name = 'None'
                    max_frags_ship_tier = '0'

                # Divider for clarity

                out_text = '```haskell'
                out_text += '\nNickname: ' + game_nickname
                out_text += '\nJoin Date: ' + join_date_conv
                out_text += '\nLevel: ' + str(leveling_tier)
                out_text += '\nDistance: ' + str(distance) + ' KM'
                out_text += '\nBattles: ' + str(battle_count)
                out_text += '\nLast Battle: ' + last_battle_conv
                out_text += '\nMax XP From a Battle: ' + str(max_xp)
                out_text += '\nMax DMG To Spotted Ship: ' + str(max_spotted_dmg)
                out_text += '\nMax Kills: ' + str(max_frags)
                out_text += '\nTotal Kills: ' + str(frags)
                out_text += '\nShip With Most Kills: ' + max_frags_ship_name + ' (Tier ' + str(max_frags_ship_tier) + ')'
                out_text += '\nTotal Shots: ' + str(shots)
                out_text += '\nTotal Hits: ' + str(hits)
                out_text += '\n```'

                # Divider for clarity

                await self.client.send_message(message.channel, out_text)
            except SyntaxError as err:
            #except Exception as err:
                print(err)
                await self.client.send_message(message.channel, 'We ran into an error, the user most likely doesn\'t exist in the region, or something dun goofed.\nError: **' + str(err) + '**')
                return


