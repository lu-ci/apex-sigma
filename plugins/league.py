from plugin import Plugin
from config import cmd_league
from config import RiotAPIKey as riot_api_key
import os
import wget
import requests
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

class LeagueOfLegends(Plugin):
    is_global = True

    async def on_message(self, message, pfx):
        # League of Legends API
        if message.content.startswith(pfx + cmd_league + ' '):
            await self.client.send_typing(message.channel)
            cmd_name = 'League of Legends'
            lol_input = str(message.content[len(pfx) + len(cmd_league) + 1:])
            region, ignore, smnr_name = lol_input.lower().partition(' ')
            smnr_name_table = smnr_name.replace(' ', '')
            smrn_by_name_url = 'https://' + region + '.api.pvp.net/api/lol/' + region + '/v1.4/summoner/by-name/' + smnr_name + '?api_key=' + riot_api_key
            if region.lower() == 'eune' or 'euw' or 'na':
                smnr_by_name = requests.get(smrn_by_name_url).json()
                smnr_id = str(smnr_by_name[smnr_name_table]['id'])
                smnr_icon = str(smnr_by_name[smnr_name_table]['profileIconId'])
                icon_url = 'http://ddragon.leagueoflegends.com/cdn/6.17.1/img/profileicon/' + smnr_icon + '.png'
                smnr_lvl = str(smnr_by_name[smnr_name_table]['summonerLevel'])
                summary_url = 'https://' + region + '.api.pvp.net/api/lol/' + region + '/v1.3/stats/by-summoner/' + smnr_id + '/summary?season=SEASON2016&api_key=' + riot_api_key
                summary = requests.get(summary_url).json()
                league_url = 'https://' + region + '.api.pvp.net/api/lol/' + region + '/v2.5/league/by-summoner/' + smnr_id + '?api_key=' + riot_api_key
                try:
                    league = requests.get(league_url).json()
                    league_name = league[smnr_id][0]['name']
                    league_tier = league[smnr_id][0]['tier']
                except:
                    league_name = 'No League'
                    league_tier = 'No Rank'
                # Image Start
                if os.path.isfile('cache/lol/avatar_' + message.author.id + '.png'):
                    os.remove('cache/lol/avatar_' + message.author.id + '.png')
                if os.path.isfile('cache/lol/profile_' + message.author.id + '.png'):
                    os.remove('cache/lol/profile_' + message.author.id + '.png')
                avaloc = 'cache/lol/avatar_' + message.author.id + '.png'
                wget.download(icon_url, out=avaloc)
                # avatar_link_base = 'https://blzgdapipro-a.akamaihd.net/game/unlocks/'
                # avatar_name = str(profile_json['data']['avatar'])
                # os.rename(avatar_name[len(avatar_link_base):], '/cache/ow/avatar_' + message.author.id + '.png')
                # border_link_base = 'https://blzgdapipro-a.akamaihd.net/game/playerlevelrewards/'
                # border_name = str(profile_json['data']['levelFrame'])
                # os.rename(border_name[len(border_link_base):], '/cache/ow/border_' + message.author.id + '.png')
                base = Image.open('img/lol/base.png')
                overlay = Image.open('img/lol/overlay_lol.png')
                background = Image.open('cache/lol/avatar_' + message.author.id + '.png')
                background_res = background.resize((72, 72), Image.ANTIALIAS)
                foreground = Image.open('img/lol/border_lol.png')
                foreground_res = foreground.resize((64, 64), Image.ANTIALIAS)
                base.paste(background_res, (28, 28))
                base.paste(overlay, (0, 0), overlay)
                base.paste(foreground_res, (32, 32), foreground_res)
                font = ImageFont.truetype("big_noodle_titling_oblique.ttf", 32)
                font2 = ImageFont.truetype("big_noodle_titling_oblique.ttf", 16)
                font3 = ImageFont.truetype("big_noodle_titling_oblique.ttf", 48)
                imgdraw = ImageDraw.Draw(base)
                imgdraw.text((130, 38), smnr_name, (255, 255, 255), font=font)
                imgdraw.text((130, 70), league_name + ' - ' + league_tier, (255, 255, 255), font=font2)
                imgdraw.text((326, 38), smnr_lvl, (255, 255, 255), font=font3)
                base.save('cache\lol\profile_' + message.author.id + '.png')
                # Image End

                try:
                    item = next((item for item in summary['playerStatSummaries'] if item['playerStatSummaryType'] == 'RankedSolo5x5'), None)
                    if item:
                        ranked = item
                        ranked_wins = str(ranked['wins'])
                        ranked_losses = str(ranked['losses'])
                        ranked_kills = str(ranked['aggregatedStats']['totalChampionKills'])
                        ranked_minions = str(ranked['aggregatedStats']['totalMinionKills'])
                        ranked_turrets = str(ranked['aggregatedStats']['totalTurretsKilled'])
                        ranked_neutrals = str(ranked['aggregatedStats']['totalNeutralMinionsKilled'])
                        ranked_assists = str(ranked['aggregatedStats']['totalAssists'])
                        ranked_text = ('Wins: ' + ranked_wins +
                                       '\nLosses: ' + ranked_losses +
                                       '\nKills: ' + ranked_kills +
                                       '\nAssists: ' + ranked_assists +
                                       '\nMinion Kills: ' + ranked_minions +
                                       '\nTurret Kills: ' + ranked_turrets +
                                       '\nJungle Minion Kills: ' + ranked_neutrals)
                    else:
                        ranked_text = 'None'
                except:
                    ranked_text = 'None'
                try:
                    item = next((item for item in summary['playerStatSummaries'] if item['playerStatSummaryType'] == 'Unranked'), None)
                    if item:
                        normal = item
                        normal_wins = str(normal['wins'])
                        normal_kills = str(normal['aggregatedStats']['totalChampionKills'])
                        normal_minions = str(normal['aggregatedStats']['totalMinionKills'])
                        normal_turrets = str(normal['aggregatedStats']['totalTurretsKilled'])
                        normal_neutrals = str(normal['aggregatedStats']['totalNeutralMinionsKilled'])
                        normal_assists = str(normal['aggregatedStats']['totalAssists'])
                        normal_text = ('Wins: ' + normal_wins +
                                       '\nKills: ' + normal_kills +
                                       '\nAssists: ' + normal_assists +
                                       '\nMinion Kills: ' + normal_minions +
                                       '\nTurret Kills: ' + normal_turrets +
                                       '\nJungle Minion Kills: ' + normal_neutrals)
                    else:
                        normal_text = 'None'
                except SyntaxError:
                    normal_text = 'None'
                if ranked_text == 'None' and normal_text == 'None':
                    await self.client.send_message(message.channel, 'No stats found.')
                else:
                    await self.client.send_file(message.channel, 'cache/lol/profile_' + message.author.id + '.png')
                    await self.client.send_message(message.channel,'Normal Stats:\n```' + normal_text + '\n```\nRanked Stats:\n```' + ranked_text + '\n```')
            else:
                await self.client.send_message(message.channel, 'Invalid Region: `' + region + '`.')
            #print('CMD [' + cmd_name + '] > ' + initiator_data)