import discord
import asyncio
import sys
import os
import time
import datetime
import json
import urllib.request
import urllib.error
import wget
from PIL import Image

print('Starting up...')
start_time = time.time()
time = time.time()
current_time = datetime.datetime.now().time()
current_time.isoformat()

if os.path.isfile('config.json') == False:
    sys.exit('Fatal Error: config.json is not present.\nIf you didn\'t already, rename config.example.json to config.json and try again.')
else:
    print('config.json present, continuing...')
if os.path.isfile('commands.json') == False:
    sys.exit('Fatal Error: commands.json is not present.\nIf you didn\'t already, rename config.example.json to config.json and try again.')
else:
    print('commands.json present, continuing...')

with open('config.json', 'r', encoding='utf-8') as config_file:
    config = config_file.read()
    config = json.loads(config)
    print('Loaded configuration.')
with open('commands.json', 'r', encoding='utf-8') as commands_file:
    commands = commands_file.read()
    commands = json.loads(commands)
    print('Loaded commands.')

token = (config['Token'])
if token == '':
    sys.exit('Token not provided, please open config.json and place your token.')
pfx = (config['Prefix'])
ownr = (config['OwnerID'])
client = discord.Client()
riot_api_key = '759fa53e-7837-4109-bf6a-05b8dc63d702'

# Commands
cmd_count = (commands['cmd_count'])
cmd_overwatch = (commands['cmd_overwatch'])
cmd_league = (commands['cmd_league'])

# I love spaghetti!

@client.event
async def on_ready():
    print('\nLogin Details:')
    print('---------------------')
    print('Logged in as:')
    print(client.user.name)
    print('Bot User ID:')
    print(client.user.id)
    print('---------------------\n')
    print('---------------------------------------')
    print('Running discord.py version ' + discord.__version__)
    print('---------------------------------------\n')
    print('STATUS: Finished Loading!')
    print('-------------------------\n')
    print('-----------------------------------------')
    print('Authors: AXAz0r, Awakening')
    print('Bot Version: Beta 0.1')
    print('Build Date: 20. August 2016.')
    print('-----------------------------------------\n')

@client.event
async def on_message(message):
    # Static Strings
    initiator_data = ('by: ' + str(message.author) + '\nUserID: ' + str(message.author.id) + '\nServer: ' + str(message.server.name) + '\nServerID: ' + str(message.server.id) + '\n-----------------------------------------')
    permission_error = ('PERMISSION DENIED!\nCommand user by: ' + str(message.author) + '\nUserID: ' + str(message.author.id) + '\nServer: ' + str(message.server.name) + '\nServerID: ' + str(message.server.id) + '\n-----------------------------------------')
    client.change_status(game=None)
    if message.content.startswith(pfx + cmd_count):
        cmd_name = 'Count'
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp,'<@' + message.author.id + '> You have written {} messages.'.format(counter))
        print('CMD [' + cmd_name + '] > ' + initiator_data)
# Overwatch API
    elif message.content.startswith(pfx + cmd_overwatch + ' '):
        cmd_name = 'Overwatch'
        await client.send_typing(message.channel)
        ow_input = (str(message.content[len(cmd_overwatch) + 1 + len(pfx):])).replace('#', '-')
        ow_region_x, ignore, ow_name = ow_input.partition(' ')
        #ow_name = (str(ow_input[3:]))
        #ow_region = (str(ow_input[:12]))
        ow_region = ow_region_x.replace('NA', 'US')
        #profile = ('https://api.lootbox.eu/pc/eu/' + ow_name + '/profile')
        profile = ('http://127.0.0.1:9000/pc/' + ow_region.lower() + '/' + ow_name + '/profile').replace(' ', '')
        profile_json_source = urllib.request.urlopen(profile).read().decode('utf-8')
        profile_json = json.loads(profile_json_source)
        try:
            avatar_link = profile_json['data']['avatar']
            border_link = profile_json['data']['levelFrame']
            if os.path.isfile('avatar.png') == True:
                os.remove('avatar.png')
            if os.path.isfile('border.png') == True:
                os.remove('border.png')
            if os.path.isfile('profile.png') == True:
                os.remove('profile.png')
            wget.download(avatar_link)
            avatar_link_base = 'https://blzgdapipro-a.akamaihd.net/game/unlocks/'
            avatar_name = str(profile_json['data']['avatar'])
            os.rename(avatar_name[len(avatar_link_base):], 'avatar.png')
            #avatar_pre_conv = Image.open('avatar.png')
            #avatar_converted = Image.new("RGB", avatar_pre_conv.size, (255,255,255))
            #avatar_converted.paste(avatar_pre_conv, (0, 0), avatar_pre_conv)
            #avatar_converted.save('avatar.png')
            wget.download(border_link)
            border_link_base = 'https://blzgdapipro-a.akamaihd.net/game/playerlevelrewards/'
            border_name = str(profile_json['data']['levelFrame'])
            os.rename(border_name[len(border_link_base):], 'border.png')
            base = Image.open('base.png')
            overlay = Image.open('overlay.png')
            foreground = Image.open('border.png')
            foreground_res = foreground.resize((128, 128), Image.ANTIALIAS)
            background = Image.open('avatar.png')
            background_res = background.resize((72, 72), Image.ANTIALIAS)
            base.paste(background_res, (28, 28))
            base.paste(overlay, (0, 0), overlay)
            base.paste(foreground_res, (0, 0), foreground_res)
            base.save('profile.png')
            if message.author.id == '152239976338161664':
                rank_error = 'Goddamn it Bubu!'
            else:
                rank_error = 'Season not active.'
            #Original Rank Code: str(profile_json['data']['games']['competitive']['lost']
            overwatch_profile = ('**Name:** ' + profile_json['data']['username'] +
                                '\n**Level:** ' + str(profile_json['data']['level']) +
                                '\n**Quick Games:**' +
                                '\n    **- Played:** ' + str(profile_json['data']['games']['quick']['played']) +
                                '\n    **- Won:** ' + str(profile_json['data']['games']['quick']['wins']) +
                                '\n    **- Lost:** ' + str(profile_json['data']['games']['quick']['lost']) +
                                '\n**Competitive Games:**' +
                                '\n    **- Played:** ' + str(profile_json['data']['games']['competitive']['played']) +
                                '\n    **- Won:** ' + str(profile_json['data']['games']['competitive']['wins']) +
                                '\n    **- Lost:** ' + str(profile_json['data']['games']['competitive']['lost']) +
                                '\n    **- Rank:** ' + rank_error +
                                '\n**Playtime:**' +
                                '\n    **- Quick:** ' +str(profile_json['data']['playtime']['quick']) +
                                '\n    **- Competitive:** ' + str(profile_json['data']['playtime']['competitive'])
                                 )
            print('CMD [' + cmd_name + '] > ' + initiator_data)
            await client.send_file(message.channel, 'profile.png')
            await client.send_message(message.channel, overwatch_profile)
        except KeyError:
            try:
                print('CMD [' + cmd_name + '] > ' + initiator_data)
                print(profile_json['error'])
                await client.send_message(message.channel, profile_json['error'])
            except:
                print('CMD [' + cmd_name + '] > ' + initiator_data)
                await client.send_message(message.channel, 'Something went wrong.\nThe servers are most likely overloaded, please try again.')
# League of Legends API
    elif message.content.startswith(pfx + cmd_league + ' '):
        await client.send_typing(message.channel)
        cmd_name = 'League of Legends'
        lol_input = (str(message.content[len(cmd_league) + 1 + len(pfx):])).replace('#', '-')
        region_x, ignore, summoner_name_x = lol_input.partition(' ')
        summoner_name = summoner_name_x.lower()
        region = region_x.lower()
        summoner_by_name = ('https://' + region + '.api.pvp.net/api/lol/' + region + '/v1.4/summoner/by-name/' + summoner_name + '?api_key=' + riot_api_key)
        print(summoner_by_name)
        summoner_by_name_json_src = urllib.request.urlopen(summoner_by_name).read().decode('utf-8')
        summoner_by_name_json = json.loads(summoner_by_name_json_src)
        try:
            smn_name = str(summoner_by_name_json[summoner_name]['name'])
            smn_id = str(summoner_by_name_json[summoner_name]['id'])
            smn_icon = str(summoner_by_name_json[summoner_name]['profileIconId'])
            smn_level = str(summoner_by_name_json[summoner_name]['summonerLevel'])

            stats_normal_url = ('https://' + region + '.api.pvp.net/api/lol/' + region + '/v1.3/stats/by-summoner/' + smn_id + '/summary?season=SEASON2016&api_key=' + riot_api_key)
            print(stats_normal_url)
            stats_normal_json = urllib.request.urlopen(stats_normal_url).read().decode('utf-8')
            stats_normal = json.loads(stats_normal_json)
            stats_ranked_url = ('https://' + region + '.api.pvp.net/api/lol/' + region + '/v1.3/stats/by-summoner/' + smn_id + '/ranked?season=SEASON2016&api_key=' + riot_api_key)
            print(stats_ranked_url)
            stats_ranked_json = urllib.request.urlopen(stats_ranked_url).read().decode('utf-8')
            stats_ranked = json.loads(stats_normal_json)

            norm_totalAssists = str(stats_ranked['playerStatSummaries'][0]['aggregatedStats']['totalAssists'])
            norm_totalNeutralMinionsKilled = str(stats_ranked['playerStatSummaries']['aggregatedStats']['totalNeutralMinionsKilled'])
            norm_totalMinionKills = str(stats_ranked['playerStatSummaries']['aggregatedStats']['totalMinionKills'])
            norm_totalChampionKills = str(stats_ranked['playerStatSummaries']['aggregatedStats']['totalChampionKills'])
            norm_totalTurretsKilled = str(stats_ranked['playerStatSummaries']['aggregatedStats']['averageAssists'])
            await client.send_message(message.channel, '**Summoner Name:** ' + smn_name +
                                    '\n**Summoner ID:** ' + smn_id +
                                    '\n**Summoner Level:** ' + smn_level +
                                    '\\n**Ranked:**' +
                                    '\n   - **Kills:** ' + norm_totalChampionKills +
                                      '\n   - **Assists:** ' + norm_totalAssists +
                                      '\n   - **Minion Kills:** ' + norm_totalMinionKills +
                                      '\n   - **Neutral Minion Kills:** ' + norm_totalNeutralMinionsKilled +
                                      '\n   - **Turret Kills:** ' + norm_totalTurretsKilled)
            print('CMD [' + cmd_name + '] > ' + initiator_data)
        except KeyError:
            try:
                print('CMD [' + cmd_name + '] > ' + initiator_data)
                print(summoner_by_name_json['error'])
                await client.send_message(message.channel, 'Error:' + summoner_by_name_json['status']['status_code'] + ' - ' + summoner_by_name_json['status']['message'] + '.')
            except:
                print('CMD [' + cmd_name + '] > ' + initiator_data)
                await client.send_message(message.channel, 'Something went wrong.\nThe servers are most likely overloaded, please try again.')
    elif message.content.startswith('-read<@92747043885314048>'):
        if message.author.id == ownr:
            await client.send_message(message.channel, 'Alex stop wasting time and get back to working on my APIs...')
        elif message.author.id == '92747043885314048':
            await client.send_message(message.channel, 'Ace, I heard Alex bought this giant black dildo, wanna go test it out?')
        else:
            await client.send_message(message.channel, 'No! ಠ_ಠ')
client.run(token)