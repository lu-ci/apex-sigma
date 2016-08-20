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

# Commands
cmd_count = (commands['cmd_count'])
cmd_overwatch = (commands['cmd_overwatch'])

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
    elif message.content.startswith(pfx + cmd_overwatch + ' '):
        cmd_name = 'Overwatch'
        client.send_typing(message.channel)
        ow_name = (str(message.content[len(cmd_overwatch) + 1 + len(pfx):])).replace('#', '-')
        profile = ('https://api.lootbox.eu/pc/eu/' + ow_name + '/profile')
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
            wget.download(border_link)
            border_link_base = 'https://blzgdapipro-a.akamaihd.net/game/playerlevelrewards/'
            border_name = str(profile_json['data']['levelFrame'])
            os.rename(border_name[len(border_link_base):], 'border.png')
            base = Image.open('base.png')
            foreground = Image.open('border.png')
            foreground_res = foreground.resize((176, 176), Image.ANTIALIAS)
            background = Image.open('avatar.png')
            background_res = background.resize((72, 72), Image.ANTIALIAS)
            base.paste(background_res, (28, 28), background_res)
            base.paste(foreground_res, (-24, -24), foreground_res)
            base.save('profile.png')
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
                                '\n    **- Rank:** ' + str(profile_json['data']['games']['competitive']['lost']) +
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
client.run(token)