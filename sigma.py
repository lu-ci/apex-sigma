# noinspection PyPep8
import datetime
import json
import os
import sys
import time
import urllib.error
import urllib.request
import discord
import lxml.html
import wget
import requests
from PIL import Image

print('Starting up...')
start_time = time.time()
time = time.time()
current_time = datetime.datetime.now().time()
current_time.isoformat()

if not os.path.isfile('config.json'):
    sys.exit('Fatal Error: config.json is not present.\nIf you didn\'t already, rename config.example.json to config.json and try again.')
else:
    print('config.json present, continuing...')
if not os.path.isfile('commands.json'):
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
mashape_key = 'nvLNoBix6DmshG97ORG4iB51mHa5p1UezKwjsnigQ85K5RXieT'
owm_key = 'b49efc119530833da61588e4d87668c1'

# Commands
cmd_count = (commands['cmd_count'])
cmd_overwatch = (commands['cmd_overwatch'])
cmd_league = (commands['cmd_league'])
cmd_bns = (commands['cmd_bns'])
cmd_ud = (commands['cmd_ud'])
cmd_weather = (commands['cmd_weather'])

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
        ow_region = ow_region_x.replace('NA', 'US')
        profile = ('http://127.0.0.1:9000/pc/' + ow_region.lower() + '/' + ow_name + '/profile').replace(' ', '')
        profile_json_source = urllib.request.urlopen(profile).read().decode('utf-8')
        profile_json = json.loads(profile_json_source)
        try:
            avatar_link = profile_json['data']['avatar']
            border_link = profile_json['data']['levelFrame']
            if os.path.isfile('avatar.png'):
                os.remove('avatar.png')
            if os.path.isfile('border.png'):
                os.remove('border.png')
            if os.path.isfile('profile.png'):
                os.remove('profile.png')
            wget.download(avatar_link)
            avatar_link_base = 'https://blzgdapipro-a.akamaihd.net/game/unlocks/'
            avatar_name = str(profile_json['data']['avatar'])
            os.rename(avatar_name[len(avatar_link_base):], 'avatar.png')
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
        if os.path.isfile('lolsig.png'):
            os.remove('lolsig.png')
        lol_input = (str(message.content[len(cmd_league) + 1 + len(pfx):]))
        region_x, ignore, summoner_name_x = lol_input.partition(' ')
        summoner_name = summoner_name_x.lower()
        region = region_x.lower()
        lol_sig_url = ('http://lolsigs.com/' + summoner_name + '_' + region + '_266_0.png')
        wget.download(lol_sig_url)
        os.rename(summoner_name + '_' + region + '_266_0.png', 'lolsig.png')
        try:
            await client.send_file(message.channel, 'lolsig.png')
            print('CMD [' + cmd_name + '] > ' + initiator_data)
        except KeyError:
            print('CMD [' + cmd_name + '] > ' + initiator_data)
            await client.send_message(message.channel, 'Something went wrong.\nThe servers are most likely overloaded, please try again.')
    elif message.content.startswith('-read<@92747043885314048>'):
        if message.author.id == ownr:
            await client.send_message(message.channel, 'Alex stop wasting time and get back to working on my APIs...')
        elif message.author.id == '92747043885314048':
            await client.send_message(message.channel, 'Ace, I heard Alex bought this giant black dildo, wanna go test it out?')
        else:
            await client.send_message(message.channel, 'No! ಠ_ಠ')
# Blade and Soul API
    elif message.content.startswith(pfx + cmd_bns + ' '):
        cmd_name = 'Blade and Soul'
        bns_input = (str(message.content[len(cmd_bns) + 1 + len(pfx):]))
        region_x, ignore, char_name_x = bns_input.partition(' ')
        char_name = char_name_x.lower()
        region = region_x.lower()
        profile_url = ('http://' + region + '-bns.ncsoft.com/ingame/bs/character/profile?c=' + char_name)
        try:
            profile_url = ('http://' + region + '-bns.ncsoft.com/ingame/bs/character/profile?c=' + char_name)
            def page_raw_data():
                page_data = urllib.request.urlopen(profile_url).read()
                return str(page_data)
            page_data_html = lxml.html.document_fromstring(page_raw_data())
            page_data_extr = page_data_html.xpath("//div[@class='stat-point]'")
            await client.send_message(message.channel, 'Retrieving data...')
            await client.send_typing(message.channel)
            print(page_data_extr)
            await client.send_message(message.channel, page_data_extr)
            print('CMD [' + cmd_name + '] > ' + initiator_data)
        except:
            client.send_message(message.channel, 'Something went wrong...')
            print('CMD [' + cmd_name + '] > ' + initiator_data)
#Urban Dictionary API
    elif message.content.startswith(pfx + cmd_ud + ' '):
        await client.send_typing(message.channel)
        cmd_name = 'Urban Dictionary'
        ud_input = (str(message.content[len(cmd_ud) + 1 + len(pfx):]))
        url = "https://mashape-community-urban-dictionary.p.mashape.com/define?term=" + ud_input
        headers = {'X-Mashape-Key': mashape_key, 'Accept': 'text/plain'}
        #r = requests.get(url, headers=headers)
        #r_dec = r.read.decode('utf-8')
        response = requests.get(url, headers=headers).json()
        result_type = str((response['result_type']))
        if result_type == 'exact':
            try:
                definition = str((response['list'][0]['definition']))
                permalink = str((response['list'][0]['permalink']))
                #thumbs_up = str((response['list'][0]['thumbs_up']))
                #thumbs_down = str((response['list'][0]['thumbs_down']))
                example = str((response['list'][0]['example']))
                await client.send_message(message.channel, 'Word: `' + ud_input + '`\n'
                                          'Definition:\n```' + definition + '```\n' +
                                          'Example:\n```' + example + '```\n' +
                                          'Source: ```' + permalink + '```')
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
        city, ignore, country = owm_input.partition(' ')
        owm_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + ',' + country + '&appid=b49efc119530833da61588e4d87668c1'
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
client.run(token)