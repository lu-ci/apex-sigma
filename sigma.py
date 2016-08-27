# noinspection PyPep8
import config as cfg
import datetime
import json
import os
import sys
import time
import urllib.error
import urllib.request
import discord
import random
import wget
import requests
import pushbullet
import googleapiclient as gapi
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import plugins.bns_api as bns_api
import plugins.youtube_api as yt_api

print('Starting up...')
start_time = time.time()
time = time.time()
current_time = datetime.datetime.now().time()
current_time.isoformat()

if not os.path.isfile('config.py'):
    sys.exit(
        'Fatal Error: config.json is not present.\nIf you didn\'t already, rename config.example.json to config.json and try again.')
else:
    print('config.py present, continuing...')
# Data
token = cfg.Token
if token == '':
    sys.exit('Token not provided, please open config.json and place your token.')
pfx = cfg.Prefix
ownr = cfg.OwnerID
client = discord.Client()
riot_api_key = cfg.RiotAPIKey
mashape_key = cfg.MashapeKey
owm_key = cfg.OpenWeatherMapKey
notify = cfg.Notifications
pb_key = cfg.Pushbullet
pb = pushbullet.Pushbullet(pb_key)
gapi = cfg.GoogleAPIKey

# Commands
cmd_help  = cfg.cmd_help
cmd_overwatch  = cfg.cmd_overwatch
cmd_league  = cfg.cmd_league
cmd_bns  = cfg.cmd_bns
cmd_ud  = cfg.cmd_ud
cmd_weather  = cfg.cmd_weather
cmd_hearthstone  = cfg.cmd_hearthstone
cmd_pokemon  = cfg.cmd_pokemon
cmd_joke  = cfg.cmd_joke

# I love spaghetti!

@client.event
async def on_ready():
    gamename = '>>help'
    game = discord.Game(name=gamename)
    await client.change_status(game)
    print('\nLogin Details:')
    print('-------------------------')
    print('Logged in as:')
    print(client.user.name)
    print('Bot User ID:')
    print(client.user.id)
    print('-------------------------\n')
    print('-------------------------')
    print('Running discord.py version\n' + discord.__version__)
    print('-------------------------')
    print('STATUS: Finished Loading!')
    print('-------------------------\n')
    print('-------------------------')
    print('Authors: AXAz0r, Awakening')
    print('Bot Version: Beta 0.16')
    print('Build Date: 24. August 2016.')
    print('-------------------------')
    if notify == 'Yes':
        pb.push_note('Sigma', 'Sigma Activated!')
    else:
        print(client.user.name + ' activated.')
    folder = 'cache/ow'
    folder2 = 'cache/lol'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        file_path2 = os.path.join(folder2, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            if os.path.isfile(file_path2):
                os.unlink(file_path2)
        except Exception as e:
            print(e)


@client.event
async def on_message(message):
    # Static Strings
    initiator_data = ('by: ' + str(message.author) + '\nUserID: ' + str(message.author.id) + '\nContent: [' + str(
        message.content) + ']\nServer: ' + str(message.server.name) + '\nServerID: ' + str(
        message.server.id) + '\n-------------------------')
    client.change_status(game=None)
    if message.content.startswith(pfx + cmd_help):
        cmd_name = 'Help'
        await client.send_typing(message.channel)
        await client.send_message(message.channel, '\nHelp: `' + pfx + cmd_help + '`' +
                                  '\nOverwatch: `' + pfx + cmd_overwatch + '`' +
                                  '\nLeague of Legends: `' + pfx + cmd_league + '`' +
                                  '\nBlade and Soul: `' + pfx + cmd_bns + '`' +
                                  '\n - Detailed Attack Stats: `' + pfx + cmd_bns + 'att' + '`' +
                                  '\n - Detailed Defense Stats: `' + pfx + cmd_bns + 'def' + '`' +
                                  '\nUrban Dictionary: `' + pfx + cmd_ud + '`' +
                                  '\nWeather: `' + pfx + cmd_weather + '`' +
                                  '\nHearthstone: `' + pfx + cmd_hearthstone + '`' +
                                  '\nPokemon: `' + pfx + cmd_pokemon + '`' +
                                  '\nJoke: `' + pfx + cmd_joke + '`')
        print('CMD [' + cmd_name + '] > ' + initiator_data)
    # Overwatch API
    elif message.content.startswith(pfx + cmd_overwatch + ' '):
        cmd_name = 'Overwatch'
        await client.send_typing(message.channel)
        ow_input = (str(message.content[len(cmd_overwatch) + 1 + len(pfx):])).replace('#', '-')
        ow_region_x, ignore, ow_name = ow_input.partition(' ')
        ow_region = ow_region_x.replace('NA', 'US')
        if os.path.isfile('cache/ow/avatar_' + message.author.id + '.png'):
            os.remove('cache/ow/avatar_' + message.author.id + '.png')
        if os.path.isfile('cache/ow/border_' + message.author.id + '.png'):
            os.remove('cache/ow/border_' + message.author.id + '.png')
        if os.path.isfile('cache/ow/profile_' + message.author.id + '.png'):
            os.remove('cache/ow/profile_' + message.author.id + '.png')
        if ow_region.upper() == 'NA' or 'US' or 'EU':
            try:
                profile = ('http://127.0.0.1:9000/pc/' + ow_region.lower() + '/' + ow_name + '/profile').replace(' ', '')
                profile_json_source = urllib.request.urlopen(profile).read().decode('utf-8')
                profile_json = json.loads(profile_json_source)
                good = True
            except:
                await client.send_message(message.channel, 'Error 503: Service unavailable.')
                good = False
            if good:
                try:
                    avatar_link = profile_json['data']['avatar']
                    border_link = profile_json['data']['levelFrame']
                    avaloc = 'cache/ow/avatar_' + message.author.id + '.png'
                    borloc = 'cache/ow/border_' + message.author.id + '.png'
                    wget.download(avatar_link, out=avaloc)
                    #avatar_link_base = 'https://blzgdapipro-a.akamaihd.net/game/unlocks/'
                    #avatar_name = str(profile_json['data']['avatar'])
                    #os.rename(avatar_name[len(avatar_link_base):], '/cache/ow/avatar_' + message.author.id + '.png')
                    wget.download(border_link, out=borloc)
                    #border_link_base = 'https://blzgdapipro-a.akamaihd.net/game/playerlevelrewards/'
                    #border_name = str(profile_json['data']['levelFrame'])
                    #os.rename(border_name[len(border_link_base):], '/cache/ow/border_' + message.author.id + '.png')
                    base = Image.open('base.png')
                    overlay = Image.open('overlay.png')
                    foreground = Image.open('cache/ow/border_' + message.author.id + '.png')
                    foreground_res = foreground.resize((128, 128), Image.ANTIALIAS)
                    background = Image.open('cache/ow/avatar_' + message.author.id + '.png')
                    background_res = background.resize((72, 72), Image.ANTIALIAS)
                    base.paste(background_res, (28, 28))
                    base.paste(overlay, (0, 0), overlay)
                    base.paste(foreground_res, (0, 0), foreground_res)
                    font = ImageFont.truetype("big_noodle_titling_oblique.ttf", 32)
                    imgdraw = ImageDraw.Draw(base)
                    imgdraw.text((130, 46), profile_json['data']['username'], (255,255,255),font=font)
                    base.save('cache\ow\profile_' + message.author.id + '.png')
                    name = profile_json['data']['username']
                    level = str(profile_json['data']['level'])
                    qg_played = str(profile_json['data']['games']['quick']['played'])
                    qg_won = str(profile_json['data']['games']['quick']['wins'])
                    qg_lost = str(profile_json['data']['games']['quick']['lost'])
                    qg_playtime = str(profile_json['data']['playtime']['quick'])
                    try:
                        cg_played = str(profile_json['data']['games']['competitive']['played'])
                    except:
                        cg_played = 'None'
                    try:
                        cg_won = str(profile_json['data']['games']['competitive']['wins'])
                    except:
                        cg_won = 'None'
                    try:
                        cg_lost = str(profile_json['data']['games']['competitive']['lost'])
                    except:
                        cg_lost = 'None'
                    try:
                        rank = str(profile_json['data']['games']['competitive']['rank'])
                    except:
                        rank = 'None'
                    try:
                        cg_playtime = str(profile_json['data']['playtime']['competitive'])
                    except:
                        cg_playtime = 'None'
                    overwatch_profile = ('```Name: ' + name +
                                         '\nLevel: ' + level +
                                         '\nQuick Games:' +
                                         '\n    - Played: ' + qg_played +
                                         '\n    - Won: ' + qg_won +
                                         '\n    - Lost: ' + qg_lost +
                                         '\nCompetitive Games:' +
                                         '\n    - Played: ' + cg_played +
                                         '\n    - Won: ' + cg_won +
                                         '\n    - Lost: ' + cg_lost +
                                         '\n    - Rank: ' + rank +
                                         '\nPlaytime:' +
                                         '\n    - Quick: ' + qg_playtime +
                                         '\n    - Competitive: ' + cg_playtime + '```')
                    print('CMD [' + cmd_name + '] > ' + initiator_data)
                    await client.send_file(message.channel, 'cache\ow\profile_' + message.author.id + '.png')
                    await client.send_message(message.channel, overwatch_profile)
                except KeyError:
                    try:
                        print('CMD [' + cmd_name + '] > ' + initiator_data)
                        print(profile_json['error'])
                        await client.send_message(message.channel, profile_json['error'])
                    except:
                        print('CMD [' + cmd_name + '] > ' + initiator_data)
                        await client.send_message(message.channel,
                                                  'Something went wrong.\nThe servers are most likely overloaded, please try again.')
            else:
                print('CMD [' + cmd_name + '] > ' + initiator_data)
        else:
            await client.send_message(message.channel, 'Invalid region: `' + ow_region.upper() + '`\nAccepted regions are `NA`, `US` and `EU`\nUsage: `' + pfx + cmd_overwatch + 'region battletag#ID')
            # League of Legends API
    elif message.content.startswith(pfx + cmd_league + ' '):
        await client.send_typing(message.channel)
        cmd_name = 'League of Legends'
        lol_input = str(message.content[len(pfx) + len(cmd_league) + 1:])
        region, ignore, smnr_name = lol_input.lower().partition(' ')
        smrn_by_name_url = 'https://' + region + '.api.pvp.net/api/lol/' + region + '/v1.4/summoner/by-name/' + smnr_name + '?api_key=' + riot_api_key
        if region.lower() == 'eune' or 'euw' or 'na':
            smnr_by_name = requests.get(smrn_by_name_url).json()
            smnr_id = str(smnr_by_name[smnr_name]['id'])
            smnr_icon = str(smnr_by_name[smnr_name]['profileIconId'])
            icon_url = 'http://ddragon.leagueoflegends.com/cdn/6.17.1/img/profileicon/' + smnr_icon + '.png'
            smnr_lvl = str(smnr_by_name[smnr_name]['summonerLevel'])
            summary_url = 'https://' + region + '.api.pvp.net/api/lol/' + region + '/v1.3/stats/by-summoner/' + smnr_id + '/summary?season=SEASON2016&api_key=' + riot_api_key
            summary = requests.get(summary_url).json()
            league_url = 'https://' + region + '.api.pvp.net/api/lol/' + region + '/v2.5/league/by-summoner/' + smnr_id + '?api_key=' + riot_api_key
            try:
                league = requests.get(league_url).json()
                league_name = league[smnr_id][0]['name']
                league_tier = league[smnr_id][0]['tier']
            except:
                league_name = 'None'
                league_tier = 'None'
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
            base = Image.open('base.png')
            overlay = Image.open('overlay_lol.png')
            background = Image.open('cache/lol/avatar_' + message.author.id + '.png')
            background_res = background.resize((72, 72), Image.ANTIALIAS)
            foreground = Image.open('border_lol.png')
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
            except SyntaxError:
                normal_text = 'None'
            if ranked_text == 'None' and normal_text == 'None':
                await client.send_message(message.channel, 'No stats found.')
            else:
                await client.send_file(message.channel, 'cache/lol/profile_' + message.author.id + '.png')
                await client.send_message(message.channel,'Normal Stats:\n```' + normal_text + '\n```\nRanked Stats:\n```' + ranked_text + '\n```')
        else:
            await client.send_message(message.channel, 'Invalid Region: `' + region + '`.')
        print('CMD [' + cmd_name + '] > ' + initiator_data)
    elif message.content.startswith('-read<@92747043885314048>'):
        if message.author.id == ownr:
            await client.send_message(message.channel, 'Alex stop wasting time and get back to working on my APIs...')
        elif message.author.id == '92747043885314048':
            await client.send_message(message.channel,
                                      'Ace, I heard Alex bought this giant black dildo, wanna go test it out?')
        else:
            await client.send_message(message.channel, 'No! ಠ_ಠ')
            # Blade and Soul API
    elif message.content.startswith(pfx + cmd_bns):
        cmd_name = 'Blade and Soul'
        await client.send_typing(message.channel)
        query = message.content[len(cmd_bns) + 1 + len(pfx):]
        region = str(query[:query.find(' ')]).lower()
        if not region == 'na' and not region == 'eu':
            error_msg = 'Invalid Region: `' + region + '`\nThe command format is `' + pfx + cmd_bns + ' [region] [Character Name]`\nThe region can be `NA` or `EU` and the character name **CAN** contain spaces.'
            await client.send_message(message.channel, error_msg)
        else:
            error_msg = 'Something went wrong, API is unavailable or character does not exist.'
            username = str(query[query.find(' ') + 1:]).lower()
            profile = bns_api.fetchStats(region, username)
            try:
                # Summary
                username = str(profile['Summary']['Username'])
                nickname = str(profile['Summary']['Nickname'])
                level = str(profile['Summary']['Level'])
                world = str(profile['Summary']['World'])
                ch_class = str(profile['Summary']['Class'])
                faction = str(profile['Summary']['Faction'])
                guild = str(profile['Summary']['Guild'])
                # Attack Stats Basic
                att_pwr = str(profile['Attack Stats']['Attack Power']['Total'])
                ev_att_rate = str(profile['Attack Stats']['Evolved Attack Rate']['Total'])
                pierc = str(profile['Attack Stats']['Piercing']['Total'])
                pierc_def = str(profile['Attack Stats']['Piercing']['Defense Piercing'])
                pierc_block = str(profile['Attack Stats']['Piercing']['Block Piercing'])
                acc = str(profile['Attack Stats']['Accuracy']['Total'])
                acc_hr = str(profile['Attack Stats']['Accuracy']['Hit Rate'])
                conc = str(profile['Attack Stats']['Concentration']['Total'])
                crit_hit = str(profile['Attack Stats']['Critical Hit']['Total'])
                crit_hit_rate = str(profile['Attack Stats']['Critical Hit']['Critical Rate'])
                crit_dmg = str(profile['Attack Stats']['Critical Damage']['Total'])
                crit_dmg_dmg = str(profile['Attack Stats']['Critical Damage']['Increase Damage'])
                mast = str(profile['Attack Stats']['Mastery']['Total'])
                add_dmg = str(profile['Attack Stats']['Additional Damage']['Total'])
                threat = str(profile['Attack Stats']['Threat']['Total'])
                fire_dmg = str(profile['Attack Stats']['Flame Damage']['Total'])
                cold_dmg = str(profile['Attack Stats']['Frost Damage']['Total'])
                # Defense Stats Basic
                hp = str(profile['Defense Stats']['HP']['Total'])
                def_tot = str(profile['Defense Stats']['Defense']['Total'])
                def_dmg_redu = str(profile['Defense Stats']['Defense']['Damage Reduction'])
                ev_def = str(profile['Defense Stats']['Evolved Defense']['Total'])
                evasion = str(profile['Defense Stats']['Evasion']['Total'])
                evasion_rate = str(profile['Defense Stats']['Evasion']['Evasion Rate'])
                block = str(profile['Defense Stats']['Block']['Total'])
                block_rate = str(profile['Defense Stats']['Block']['Block Rate'])
                crit_def = str(profile['Defense Stats']['Critical Defense']['Total'])
                crit_def_rate = str(profile['Defense Stats']['Critical Defense']['Critical Evasion Rate'])
                will = str(profile['Defense Stats']['Willpower']['Total'])
                dmg_redu = str(profile['Defense Stats']['Damage Reduction']['Total'])
                regen = str(profile['Defense Stats']['Health Regen']['Total'])
                rec = str(profile['Defense Stats']['Recovery']['Total'])
                nerf_def = str(profile['Defense Stats']['Debuff Defense']['Total'])
                # Texts
                summary_text = (':ticket: Summary:\n```' +
                                '\nUsername: ' + username +
                                '\nNickname: ' + nickname +
                                '\nLevel: ' + level +
                                '\nWorld: ' + world +
                                '\nClass: ' + ch_class +
                                '\nFaction: ' + faction +
                                '\nGuild: ' + guild +
                                '\n```')

                attack_stats_text = (':crossed_swords: Attack Stats: \n```' +
                                     '\nAttack Power: ' + att_pwr +
                                     '\nEvolved Attack Rate: ' + ev_att_rate +
                                     '\nPiercing: ' + pierc + '(DEF:' + pierc_def + '|Block: ' + pierc_block + ')' +
                                     '\nAccuracy: ' + acc + '(' + acc_hr + ')' +
                                     '\nConcentrationr: ' + conc +
                                     '\nCrtitical Hit: ' + crit_hit + '(' + crit_hit_rate + ')' +
                                     '\nCritical Damage: ' + crit_dmg + '(' + crit_dmg_dmg + ')' +
                                     '\nMastery: ' + mast +
                                     '\nAdditional Damage: ' + add_dmg +
                                     '\nThreat: ' + threat +
                                     '\nFlame Damage: ' + fire_dmg +
                                     '\nFrost Damage: ' + cold_dmg +
                                     '\n```')
                def_stats_text = (':shield: Defense Stats: \n```' +
                                  '\nHP: ' + hp +
                                  '\nDefense: ' + def_tot + '(' + def_dmg_redu + ')' +
                                  '\nEvolved Defense: ' + ev_def +
                                  '\nEvasion: ' + evasion + '(' + evasion_rate + ')' +
                                  '\nBlock: ' + block + '(' + block_rate + ')' +
                                  '\nCritical Defense: ' + crit_def + '(' + crit_def_rate + ')' +
                                  '\nWillpower: ' + will +
                                  '\nDamage Reduction: ' + dmg_redu +
                                  '\nHealth Regen: ' + regen +
                                  '\nRecovery: ' + rec +
                                  '\nDebuff Defense: ' + nerf_def +
                                  '\n```')
                await client.send_message(message.channel, summary_text + attack_stats_text + def_stats_text)
                # await client.send_message(message.channel, summary_text)
                # await client.send_message(message.channel, attack_stats_text)
                # await client.send_message(message.channel, def_stats_text)
            except:
                await client.send_message(message.channel, error_msg)
        print('CMD [' + cmd_name + '] > ' + initiator_data)
    # Blade and Soul Attack Details API
    elif message.content.startswith(pfx + 'att' + cmd_bns):
        cmd_name = 'Blade and Soul Attack Details'
        await client.send_typing(message.channel)
        query = message.content[len(cmd_bns) + 1 + 3 + len(pfx):]
        region = str(query[:query.find(' ')]).lower()
        if not region == 'na' and not region == 'eu':
            error_msg = 'Invalid Region: `' + region + '`\nThe command format is `' + pfx + cmd_bns + ' [region] [Character Name]`\nThe region can be `NA` or `EU` and the character name **CAN** contain spaces.'
            await client.send_message(message.channel, error_msg)
        else:
            error_msg = 'Something went wrong, API is unavailable or character does not exist.'
            username = str(query[query.find(' ') + 1:]).lower()
            profile = bns_api.fetchStats(region, username)
            try:
                # Summary
                nickname = str(profile['Summary']['Nickname'])
                # Attack Stats
                att_pwr = str(profile['Attack Stats']['Attack Power']['Total'])
                att_pwr_base = str(profile['Attack Stats']['Attack Power']['Base'])
                att_pwr_eqp = str(profile['Attack Stats']['Attack Power']['Equipped'])
                ev_att_rate = str(profile['Attack Stats']['Evolved Attack Rate']['Total'])
                ev_att_rate_base = str(profile['Attack Stats']['Evolved Attack Rate']['Base'])
                ev_att_rate_eqp = str(profile['Attack Stats']['Evolved Attack Rate']['Equipped'])
                pierc = str(profile['Attack Stats']['Piercing']['Total'])
                pierc_base = str(profile['Attack Stats']['Piercing']['Base'])
                pierc_eqp = str(profile['Attack Stats']['Piercing']['Equipped'])
                pierc_def = str(profile['Attack Stats']['Piercing']['Defense Piercing'])
                pierc_block = str(profile['Attack Stats']['Piercing']['Block Piercing'])
                acc = str(profile['Attack Stats']['Accuracy']['Total'])
                acc_base = str(profile['Attack Stats']['Accuracy']['Base'])
                acc_eqp = str(profile['Attack Stats']['Accuracy']['Equipped'])
                acc_hr = str(profile['Attack Stats']['Accuracy']['Hit Rate'])
                conc = str(profile['Attack Stats']['Concentration']['Total'])
                conc_base = str(profile['Attack Stats']['Concentration']['Base'])
                conc_eqp = str(profile['Attack Stats']['Concentration']['Equipped'])
                conc_bsp = str(profile['Attack Stats']['Concentration']['Block Skill Piercing'])
                conc_csp = str(profile['Attack Stats']['Concentration']['Counter Skill Piercing'])
                crit_hit = str(profile['Attack Stats']['Critical Hit']['Total'])
                crit_hit_base = str(profile['Attack Stats']['Critical Hit']['Base'])
                crit_hit_eqp = str(profile['Attack Stats']['Critical Hit']['Equipped'])
                crit_hit_rate = str(profile['Attack Stats']['Critical Hit']['Critical Rate'])
                crit_dmg = str(profile['Attack Stats']['Critical Damage']['Total'])
                crit_dmg_base = str(profile['Attack Stats']['Critical Damage']['Base'])
                crit_dmg_eqp = str(profile['Attack Stats']['Critical Damage']['Equipped'])
                crit_dmg_dmg = str(profile['Attack Stats']['Critical Damage']['Increase Damage'])
                mast = str(profile['Attack Stats']['Mastery']['Total'])
                add_dmg = str(profile['Attack Stats']['Additional Damage']['Total'])
                add_dmg_bonus = str(profile['Attack Stats']['Additional Damage']['Damage Bonus'])
                threat = str(profile['Attack Stats']['Threat']['Total'])
                threat_base = str(profile['Attack Stats']['Threat']['Base'])
                threat_eqp = str(profile['Attack Stats']['Threat']['Equipped'])
                threat_bonus = str(profile['Attack Stats']['Threat']['Threat Bonus'])
                fire_dmg = str(profile['Attack Stats']['Flame Damage']['Total'])
                fire_dmg_base = str(profile['Attack Stats']['Flame Damage']['Base'])
                fire_dmg_eqp = str(profile['Attack Stats']['Flame Damage']['Equipped'])
                fire_dmg_rate = str(profile['Attack Stats']['Flame Damage']['Flame Damage Rate'])
                cold_dmg = str(profile['Attack Stats']['Frost Damage']['Total'])
                cold_dmg_base = str(profile['Attack Stats']['Frost Damage']['Base'])
                cold_dmg_eqp = str(profile['Attack Stats']['Frost Damage']['Equipped'])
                cold_dmg_rate = str(profile['Attack Stats']['Frost Damage']['Frost Damage Rate'])
                attack_stats_text = (':crossed_swords: Attack Stats for **' + nickname + '**: \n```' +
                                     '\nAttack Power: ' + att_pwr +
                                     '\n(Base: ' + att_pwr_base + '|Equipped: ' + att_pwr_eqp + ')' +
                                     '\nEvolved Attack Rate: ' + ev_att_rate +
                                     '\n(Base: ' + ev_att_rate_base + '|Equipped: ' + ev_att_rate_eqp + ')' +
                                     '\nPiercing: ' + pierc +
                                     '\n(Base: ' + pierc_base + '|Equipped: ' + pierc_eqp + '|DEF: ' + pierc_def + '|Block: ' + pierc_block + ')' +
                                     '\nAccuracy: ' + acc +
                                     '\n(Base: ' + acc_base + '|Equipped: ' + acc_eqp + '|Rate: ' + acc_hr + ')' +
                                     '\nConcentrationr: ' + conc +
                                     '\n(Base: ' + conc_base + '|Equipped: ' + conc_eqp + '|BSP: ' + conc_bsp + '|CSP: ' + conc_csp + ')' +
                                     '\nCrtitical Hit: ' + crit_hit +
                                     '\n(Base: ' + crit_hit_base + '|Equipped: ' + crit_hit_eqp + '|Rate:' + crit_hit_rate + ')' +
                                     '\nCritical Damage: ' + crit_dmg +
                                     '\n(Base: ' + crit_dmg_base + '|Equipped: ' + crit_dmg_eqp + '|DMG: ' + crit_dmg_dmg + ')' +
                                     '\nMastery: ' + mast +
                                     '\nAdditional Damage: ' + add_dmg +
                                     '\n(DMG Bonus: ' + add_dmg_bonus + ')' +
                                     '\nThreat: ' + threat +
                                     '\n(Base: ' + threat_base + '|Equipped: ' + threat_eqp + '|Bonus:' + threat_bonus + ')' +
                                     '\nFlame Damage: ' + fire_dmg +
                                     '\n(Base: ' + fire_dmg_base + '|Equipped: ' + fire_dmg_eqp + '|Rate: ' + fire_dmg_rate + ')' +
                                     '\nFrost Damage: ' + cold_dmg +
                                     '\n(Base: ' + cold_dmg_base + '|Equipped: ' + cold_dmg_eqp + '|Rate: ' + cold_dmg_rate + ')' +
                                     '\n```')
                await client.send_message(message.channel, attack_stats_text)
            except:
                await client.send_message(message.channel, error_msg)
        print('CMD [' + cmd_name + '] > ' + initiator_data)
    # Blade and Soul Defense Details API
    elif message.content.startswith(pfx + 'def' + cmd_bns):
        cmd_name = 'Blade and Soul Defense Details'
        await client.send_typing(message.channel)
        query = message.content[len(cmd_bns) + 1 + 3 + len(pfx):]
        region = str(query[:query.find(' ')]).lower()
        if not region == 'na' and not region == 'eu':
            error_msg = 'Invalid Region: `' + region + '`\nThe command format is `' + pfx + cmd_bns + ' [region] [Character Name]`\nThe region can be `NA` or `EU` and the character name **CAN** contain spaces.'
            await client.send_message(message.channel, error_msg)
        else:
            error_msg = 'Something went wrong, API is unavailable or character does not exist.'
            username = str(query[query.find(' ') + 1:]).lower()
            profile = bns_api.fetchStats(region, username)
            try:
                # Summary
                nickname = str(profile['Summary']['Nickname'])
                # Defense Stats
                hp = str(profile['Defense Stats']['HP']['Total'])
                hp_base = str(profile['Defense Stats']['HP']['Base'])
                hp_eqp = str(profile['Defense Stats']['HP']['Equipped'])
                def_tot = str(profile['Defense Stats']['Defense']['Total'])
                def_base = str(profile['Defense Stats']['Defense']['Base'])
                def_eqp = str(profile['Defense Stats']['Defense']['Equipped'])
                def_dmg_redu = str(profile['Defense Stats']['Defense']['Damage Reduction'])
                def_aoe = str(profile['Defense Stats']['Defense']['AoE Defense'])
                def_aoe_redu = str(profile['Defense Stats']['Defense']['AoE Defense Reduction'])
                ev_def = str(profile['Defense Stats']['Evolved Defense']['Total'])
                ev_def_base = str(profile['Defense Stats']['Evolved Defense']['Base'])
                ev_def_eqp = str(profile['Defense Stats']['Evolved Defense']['Equipped'])
                ev_def_rate = str(profile['Defense Stats']['Evolved Defense']['Evolved Defense Rate'])
                ev_def_aoe = str(profile['Defense Stats']['Evolved Defense']['AoE Defense'])
                ev_def_aoe_dmg_redu = str(profile['Defense Stats']['Evolved Defense']['AoE Defense Reduction'])
                evasion = str(profile['Defense Stats']['Evasion']['Total'])
                evasion_base = str(profile['Defense Stats']['Evasion']['Base'])
                evastion_eqp = str(profile['Defense Stats']['Evasion']['Equipped'])
                evasion_rate = str(profile['Defense Stats']['Evasion']['Evasion Rate'])
                evasion_ctr = str(profile['Defense Stats']['Evasion']['Counter Bonus'])
                block = str(profile['Defense Stats']['Block']['Total'])
                block_base = str(profile['Defense Stats']['Block']['Base'])
                block_eqp = str(profile['Defense Stats']['Block']['Equipped'])
                block_rate = str(profile['Defense Stats']['Block']['Block Rate'])
                block_bonus = str(profile['Defense Stats']['Block']['Block Bonus'])
                block_dmg_redu = str(profile['Defense Stats']['Block']['Damage Reduction'])
                crit_def = str(profile['Defense Stats']['Critical Defense']['Total'])
                crit_def_rate = str(profile['Defense Stats']['Critical Defense']['Critical Evasion Rate'])
                crit_def_dmg_redu = str(profile['Defense Stats']['Critical Defense']['Damage Reduction'])
                will = str(profile['Defense Stats']['Willpower']['Total'])
                dmg_redu = str(profile['Defense Stats']['Damage Reduction']['Total'])
                dmg_redu_dmg_redu = str(profile['Defense Stats']['Damage Reduction']['Damage Reduction'])
                regen = str(profile['Defense Stats']['Health Regen']['Total'])
                regen_in = str(profile['Defense Stats']['Health Regen']['In Combat'])
                regen_out = str(profile['Defense Stats']['Health Regen']['Out of Combat'])
                rec = str(profile['Defense Stats']['Recovery']['Total'])
                rec_pt = str(profile['Defense Stats']['Recovery']['Recovery'])
                rec_add = str(profile['Defense Stats']['Recovery']['Additional Recovery'])
                rec_rate = str(profile['Defense Stats']['Recovery']['Recovery Rate'])
                nerf_def = str(profile['Defense Stats']['Debuff Defense']['Total'])
                nerf_def_rate = str(profile['Defense Stats']['Debuff Defense']['Debuff Defense Rate'])
                def_stats_text = (':shield: Defense Stats for **' + nickname + '**: \n```' +
                                  '\nHP: ' + hp +
                                  '\n(Base: ' + hp_base + '|Equipped: ' + hp_eqp + ')' +
                                  '\nDefense: ' + def_tot +
                                  '\n(Base: ' + def_base + '|Equipped: ' + def_eqp + '|DMG Reduction: ' + def_dmg_redu + '|AoE DEF: ' + def_aoe + '|AoE DMG Reduction: ' + def_aoe_redu + ')' +
                                  '\nEvolved Defense: ' + ev_def +
                                  '\n(Base: ' + ev_def_base + '|Equipped: ' + ev_def_eqp + '|Defense Rate: ' + ev_def_rate + '|AoE Defense: ' + ev_def_aoe + '|AoE DMG Reduction: ' + ev_def_aoe_dmg_redu + ')' +
                                  '\nEvasion: ' + evasion +
                                  '\n(Base: ' + evasion_base + '|Equipped: ' + evastion_eqp + '|Rate: ' + evasion_rate + '|Counter Bonus: ' + evasion_ctr + ')' +
                                  '\nBlock: ' + block +
                                  '\n(Base: ' + block_base + '|Equipped: ' + block_eqp + '|DMG Redu: ' + block_dmg_redu + '|Bonus: ' + block_bonus + '|Rate: ' + block_rate + ')' +
                                  '\nCritical Defense: ' + crit_def +
                                  '\n(Rate: ' + crit_def_rate + '|DMG Reduction: ' + crit_def_dmg_redu + ')' +
                                  '\nWillpower: ' + will +
                                  '\nDamage Reduction: ' + dmg_redu +
                                  '\n(DMG Redu: ' + dmg_redu_dmg_redu + ')' +
                                  '\nHealth Regen: ' + regen +
                                  '\n(Out of Combat: ' + regen_out + '|In Combat: ' + regen_in + ')' +
                                  '\nRecovery: ' + rec +
                                  '\n(Recovery: ' + rec_pt + '|Additional: ' + rec_add + '|Rate: ' + rec_rate + ')' +
                                  '\nDebuff Defense: ' + nerf_def +
                                  '\n(Rate: ' + nerf_def_rate + ')' +
                                  '\n```')
                await client.send_message(message.channel, def_stats_text)
            except:
                await client.send_message(message.channel, error_msg)
        print('CMD [' + cmd_name + '] > ' + initiator_data)
    # Urban Dictionary API
    elif message.content.startswith(pfx + cmd_ud + ' '):
        await client.send_typing(message.channel)
        cmd_name = 'Urban Dictionary'
        ud_input = (str(message.content[len(cmd_ud) + 1 + len(pfx):]))
        url = "https://mashape-community-urban-dictionary.p.mashape.com/define?term=" + ud_input
        headers = {'X-Mashape-Key': mashape_key, 'Accept': 'text/plain'}
        # r = requests.get(url, headers=headers)
        # r_dec = r.read.decode('utf-8')
        response = requests.get(url, headers=headers).json()
        result_type = str((response['result_type']))
        if result_type == 'exact':
            try:
                definition = str((response['list'][0]['definition']))
                # permalink = str((response['list'][0]['permalink']))
                # thumbs_up = str((response['list'][0]['thumbs_up']))
                # thumbs_down = str((response['list'][0]['thumbs_down']))
                example = str((response['list'][0]['example']))
                await client.send_message(message.channel, 'Word: `' + ud_input + '`\n'
                                                                                  'Definition:\n```' + definition + '```\n' +
                                          'Example:\n```' + example + '\n```')
                print('CMD [' + cmd_name + '] > ' + initiator_data)
            except IndexError:
                await client.send_message(message.channel, 'Something went wrong... The API dun goofed...')
                print('CMD [' + cmd_name + '] > ' + initiator_data)
        elif result_type == 'no_results':
            try:
                await client.send_message(message.channel, 'No results :cry:')
                print('CMD [' + cmd_name + '] > ' + initiator_data)
            except:
                await client.send_message(message.channel, 'Something went wrong, and we don\'t know what!')
                print('CMD [' + cmd_name + '] > ' + initiator_data)
    elif message.content.startswith(pfx + cmd_weather + ' '):
        await client.send_typing(message.channel)
        cmd_name = 'Weather'
        owm_input = (str(message.content[len(cmd_weather) + 1 + len(pfx):]))
        city, ignore, country = owm_input.partition(', ')
        owm_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + ',' + country + '&appid=' + owm_key
        owm_data = urllib.request.urlopen(owm_url).read().decode('utf-8')
        owm_json = json.loads(owm_data)
        kelvin = 273.16
        try:
            coord_lon = str(owm_json['coord']['lon'])
            coord_lat = str(owm_json['coord']['lat'])
            sys_country = str(owm_json['sys']['country'])
            sys_city = str(owm_json['name'])
            weather = str(owm_json['weather'][0]['main'])
            temp = (str(round(owm_json['main']['temp'] - kelvin)) + '°C')
            temp_f = (str(round((((owm_json['main']['temp'] - kelvin) * 9) / 5) + 32)) + '°F')
            humidity = (str(owm_json['main']['humidity']) + '%')
            pressure = (str(owm_json['main']['pressure']) + ' mb')
            temp_min_c = (str(round(owm_json['main']['temp_min'] - kelvin)) + '°C')
            temp_max_c = (str(round(owm_json['main']['temp_max'] - kelvin)) + '°C')
            temp_min_f = (str(round((((owm_json['main']['temp_min'] - kelvin) * 9) / 5) + 32)) + '°F')
            temp_max_f = (str(round((((owm_json['main']['temp_max'] - kelvin) * 9) / 5) + 32)) + '°F')
            if weather == 'Thunderstorm':
                icon = ':thunder_cloud_rain:'
            elif weather == 'Drizzle':
                icon = ':cloud:'
            elif weather == 'Rain':
                icon = ':cloud_rain:'
            elif weather == 'Snow':
                icon = ':cloud_snow:'
            elif weather == 'Clear':
                icon = ':sunny:'
            elif weather == 'Clouds':
                icon = ':white_sun_cloud:'
            elif weather == 'Extreme':
                icon = ':cloud_tornado:'
            else:
                icon = ':earth_americas:'
            weather_message = ('Weather in `' + sys_city + ', ' + sys_country + '` ' +
                               'Lat: `' + coord_lat + '` | Lon: `' + coord_lon + '`\n\n' +
                               'Current State: `' + weather + '` ' + icon + '\n\n' +
                               'Details:\n```Current: ' + temp + ' (' + temp_f + ')\n' +
                               'High: ' + temp_max_c + ' (' + temp_max_f + ')\n' +
                               'Low: ' + temp_min_c + ' (' + temp_min_f + ')\n' +
                               'Humidity: ' + humidity + '\nPressure: ' + pressure + '\n```')
            await client.send_message(message.channel, weather_message)
            print('CMD [' + cmd_name + '] > ' + initiator_data)
        except AttributeError:
            await client.send_message(message.channel, 'Something went wrong, and we don\'t know what!')
            print('CMD [' + cmd_name + '] > ' + initiator_data)
        try:
            owm_error_code = str(owm_json['cod'])
            if owm_error_code == '404':
                await client.send_message(message.channel, 'Error: Requested location not found!')
                print('CMD [' + cmd_name + '] > ' + initiator_data)
        except AttributeError:
            await client.send_message(message.channel, 'Something went wrong, and we don\'t know what!')
            print('CMD [' + cmd_name + '] > ' + initiator_data)
    elif message.content.startswith(pfx + cmd_hearthstone + ' '):
        await client.send_typing(message.channel)
        cmd_name = 'Hearthstone'
        hs_input = (str(message.content[len(cmd_hearthstone) + 1 + len(pfx):]))
        url = "https://omgvamp-hearthstone-v1.p.mashape.com/cards/search/" + hs_input
        headers = {'X-Mashape-Key': mashape_key, 'Accept': 'text/plain'}
        response = requests.get(url, headers=headers).json()
        try:
            name = str(response[0]['name'])
            cardset = str(response[0]['cardSet'])
            rarity = str(response[0]['rarity'])
            cd_type = str(response[0]['type'])
            try:
                cost = str(response[0]['cost'])
            except:
                cost = '0'
            try:
                faction = str(response[0]['faction'])
            except:
                faction = 'None'
            try:
                description = str(response[0]['flavor'])
            except:
                description = 'None'
            if cd_type == 'Minion':
                attack = str(response[0]['attack'])
                health = str(response[0]['health'])
                message_text = ('Name: `' + name + '`\n' +
                                '\nType: `' + cd_type + '`' +
                                '\nFaction: `' + faction + '`' +
                                '\nRarity: `' + rarity + '`' +
                                '\nCard Set: `' + cardset + '`' +
                                '\nCost: `' + cost + '`' +
                                '\nAttack: `' + attack + '`' +
                                '\nHealth: `' + health + '`\n' +
                                '\nDescription:```\n' + description + '```')
            elif cd_type == 'Spell':
                try:
                    text = str(response[0]['text'])
                except:
                    text = 'None'
                message_text = ('Name: `' + name + '`\n' +
                                '\nType: `' + cd_type + '`' +
                                '\nFaction: `' + faction + '`' +
                                '\nRarity: `' + rarity + '`' +
                                '\nCard Set: `' + cardset + '`' +
                                '\nCost: `' + cost + '`' +
                                '\nText: \n```' + text + '\n```' +
                                '\nDescription:```\n' + description + '```')
            elif cd_type == 'Weapon':
                attack = str(response[0]['attack'])
                durability = str(response[0]['durability'])
                try:
                    text = str(response[0]['text'])
                except:
                    text = 'None'
                message_text = ('Name: `' + name + '`\n' +
                                '\nType: `' + cd_type + '`' +
                                '\nFaction: `' + faction + '`' +
                                '\nRarity: `' + rarity + '`' +
                                '\nCard Set: `' + cardset + '`' +
                                '\nCost: `' + cost + '`' +
                                '\nAttack: `' + attack + '`' +
                                '\nDurability: `' + durability + '`' +
                                '\nText: `' + text + '`' +
                                '\nDescription:```\n' + description + '```')
            else:
                message_text = 'Data incomplete or special, uncollectable card...'
            await client.send_message(message.channel, message_text)
            print('CMD [' + cmd_name + '] > ' + initiator_data)
        except:
            try:
                error = str(response['error'])
                err_message = str(response['message'])
                await client.send_message(message.channel, 'Error: ' + error + '. ' + err_message)
            except:
                await client.send_message(message.channel, 'Something went wrong...')
            print('CMD [' + cmd_name + '] > ' + initiator_data)
    elif message.content.startswith('(╯°□°）╯︵ ┻━┻'):
        await client.send_message(message.channel, '┬─┬﻿ ノ( ゜-゜ノ)')
    elif message.content.startswith(pfx + cmd_pokemon + ' '):
        await client.send_typing(message.channel)
        cmd_name = 'Pokemon'
        poke_input = (str(message.content[len(cmd_pokemon) + 1 + len(pfx):]))
        pokemon_url = ('http://pokeapi.co/api/v2/pokemon/' + poke_input.lower() + '/')
        poke = requests.get(pokemon_url).json()
        try:
            poke_id = str(poke['id'])
            name = str(poke['name']).title()
            number = '#' + str(poke['order'])
            height = str(poke['height'] / 10) + 'm'
            weight = str(poke['weight'] / 10) + 'kg'
            try:
                ability_1 = str(poke['abilities'][0]['ability']['name']).title()
                abil_1_vis = poke['abilities'][0]['is_hidden']
            except:
                ability_1 = str('None')
                abil_1_vis = False
            if abil_1_vis:
                a1v = 'Hidden'
            else:
                a1v = 'Not Hidden'
            try:
                abil_2_vis = poke['abilities'][1]['is_hidden']
            except:
                abil_2_vis = False
            if abil_2_vis:
                a2v = 'Hidden'
            else:
                a2v = 'Not Hidden'
            try:
                ability_2 = str(poke['abilities'][1]['ability']['name']).title()
            except:
                ability_2 = str('None')
            try:
                type_1 = str(poke['types'][0]['type']['name']).title()
            except:
                type_1 = str('None')
            # Icons
            if type_1 == 'Fire':
                icon_1 = ':fire:'
            elif type_1 == 'Fighting':
                icon_1 = ':muscle:'
            elif type_1 == 'Water':
                icon_1 = ':ocean:'
            elif type_1 == 'Flying':
                icon_1 = ':bird:'
            elif type_1 == 'Grass':
                icon_1 = ':herb:'
            elif type_1 == 'Poison':
                icon_1 = ':skull_crossbones:'
            elif type_1 == 'Electric':
                icon_1 = ':zap:'
            elif type_1 == 'Ground':
                icon_1 = ':chestnut:'
            elif type_1 == 'Psychic':
                icon_1 = ':eye:'
            elif type_1 == 'Rock':
                icon_1 = ':moyai:'
            elif type_1 == 'Ice':
                icon_1 = ':snowflake:'
            elif type_1 == 'Bug':
                icon_1 = ':bug:'
            elif type_1 == 'Dragon':
                icon_1 = ':dragon:'
            elif type_1 == 'Ghost':
                icon_1 = ':ghost:'
            elif type_1 == 'Dark':
                icon_1 = ':dark_sunglasses:'
            elif type_1 == 'Steel':
                icon_1 = ':nut_and_bolt:'
            elif type_1 == 'Fairy':
                icon_1 = ':gift_heart:'
            elif type_1 == 'None':
                icon_1 = 'None'
            else:
                icon_1 = ':necktie:'
            try:
                type_2 = str(poke['types'][1]['type']['name']).title()
            except:
                type_2 = str('None')
            if type_2 == 'Fire':
                icon_2 = ':fire:'
            elif type_2 == 'Fighting':
                icon_2 = ':muscle:'
            elif type_2 == 'Water':
                icon_2 = ':ocean:'
            elif type_2 == 'Flying':
                icon_2 = ':bird:'
            elif type_2 == 'Grass':
                icon_2 = ':herb:'
            elif type_2 == 'Poison':
                icon_2 = ':skull_crossbones:'
            elif type_2 == 'Electric':
                icon_2 = ':zap:'
            elif type_2 == 'Ground':
                icon_2 = ':chestnut:'
            elif type_2 == 'Psychic':
                icon_2 = ':eye:'
            elif type_2 == 'Rock':
                icon_2 = ':moyai:'
            elif type_2 == 'Ice':
                icon_2 = ':snowflake:'
            elif type_2 == 'Bug':
                icon_2 = ':bug:'
            elif type_2 == 'Dragon':
                icon_2 = ':dragon:'
            elif type_2 == 'Ghost':
                icon_2 = ':ghost:'
            elif type_2 == 'Dark':
                icon_2 = ':dark_sunglasses:'
            elif type_2 == 'Steel':
                icon_2 = ':nut_and_bolt:'
            elif type_2 == 'Fairy':
                icon_2 = ':gift_heart:'
            elif type_2 == 'None':
                icon_2 = 'None'
            else:
                icon_2 = ':necktie:'
            message_text = (' Name: `' + name + '` `' + number + '`\n' +
                            'ID: `' + poke_id + '`' +
                            '\nDetails:' +
                            '\nHeight: ' + height +
                            '\nWeight: ' + weight +
                            '\nType: ' + type_1 + '/' + type_2 + ' (' + icon_1 + '/' + icon_2 + ')' +
                            '\nAbilities: ' + ability_1 + ' (' + a1v + ') | ' + ability_2 + ' (' + a2v + ')\nImage: https://randompokemon.com/sprites/animated/' + poke_id + '.gif')
            await client.send_message(message.channel, message_text)
        except:
            try:
                await client.send_message(message.channel, str(poke['detail']))
            except:
                await client.send_message(message.channel, 'Something went wrong')
        print('CMD [' + cmd_name + '] > ' + initiator_data)
    elif message.content.startswith(pfx + 'checkbullet'):
        cmd_name = 'PushBullet Message Check'
        await client.send_typing(message.channel)
        pushes = pb.get_pushes(limit=1)
        title = pushes[0]['title']
        body = pushes[0]['body']
        await client.send_message(message.channel, 'Title: `' + title + '`\nMessage: `' + body + '`')
        pb.dismiss_push(pushes[0]['iden'])
        print('CMD [' + cmd_name + '] > ' + initiator_data)
    elif message.content.startswith(pfx + 'sendbullet'):
        cmd_name = 'PushBullet Message Send'
        await client.send_typing(message.channel)
        try:
            push_input = message.content[len(pfx) + 11:]
            title, ignore, body = str(push_input).partition(' ')
            pb.push_note(title, body)
            await client.send_message(message.channel, 'Message has been sent to <@' + ownr + '>')
        except pushbullet.errors.PushbulletError:
            await client.send_message(message.channel, 'There was a problem, probably rate limiting...')
        print('CMD [' + cmd_name + '] > ' + initiator_data)
    elif message.content.startswith(pfx + cmd_joke):
        cmd_name = 'Joke'
        number_list = [0, 1, 2]
        joke_no = random.choice(number_list)
        await client.send_typing(message.channel)
        if joke_no == 0:
            joke_type = 'Chuck Noris Joke'
            joke_url = 'https://api.chucknorris.io/jokes/random'
            joke_json = requests.get(joke_url).json()
            joke = joke_json['value']
        elif joke_no == 1:
            joke_type = 'Ron Swanson Quote'
            joke_url = 'http://ron-swanson-quotes.herokuapp.com/v2/quotes'
            joke_json = requests.get(joke_url).json()
            joke = joke_json[0]
        elif joke_no == 2:
            comic_no = str(random.randint(1, 1724))
            joke_type = 'xkcd Story'
            joke_url = 'http://xkcd.com/' + comic_no + '/info.0.json'
            joke_json = requests.get(joke_url).json()
            joke = ('#' + comic_no + ' - ' + joke_json['title'] + '\n\n' + joke_json['transcript'])
        else:
            joke_type = 'Normal Joke'
            joke_url = 'http://tambal.azurewebsites.net/joke/random'
            joke_json = requests.get(joke_url).json()
            joke = joke_json['joke']
        await client.send_message(message.channel, 'Here, have a ' + joke_type + '!\n```' + joke + '\n```')
        print('CMD [' + cmd_name + '] > ' + initiator_data)
client.run(token)