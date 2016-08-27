# noinspection PyPep8
from config import *
from commands import *
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
#import googleapiclient as g_api
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
#import plugins.youtube_api as yt_api

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
from config import Token as token
if token == '': sys.exit('Token not provided, please open config.json and place your token.')

from config import Prefix as pfx
from config import OwnerID as ownr

#from config import Pushbullet as pb_key
#pb = pushbullet.Pushbullet(pb_key)

from plugin_manager import PluginManager
from plugins.help import Help
from plugins.league import LeagueOfLegends
from plugins.bns import BladeAndSoul
from plugins.urbandictionary import UrbanDictionary
from plugins.weather import Weather
from plugins.hearthstone import Hearthstone
from plugins.pokemon import Pokemon
from plugins.joke import Joke
from plugins.overwatch import Overwatch


# I love spaghetti!
class sigma(discord.Client):

    def __init__(self):
        super().__init__()
        self.plugin_manager = PluginManager(self)
        self.plugin_manager.load_all()

    async def get_plugins(self):
        plugins = await self.plugin_manager.get_all()
        return plugins

    async def on_ready(self):
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
        print('Bot Version: Beta 0.14')
        print('Build Date: 24. August 2016.')
        print('-------------------------')
        #try:
            #if notify == 'Yes':
            #    pb.push_note('Sigma', 'Sigma Activated!')
            #else: print(client.user.name + ' activated.')
        #except: pass
        folder = 'cache/ow'
        try:
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)
        except FileNotFoundError: pass

    async def on_message(self, message):
        # Static Strings
        #initiator_data = ('by: ' + str(message.author) + '\nUserID: ' + str(message.author.id) + '\nContent: [' + str(
        #    message.content) + ']\nServer: ' + str(message.server.name) + '\nServerID: ' + str(
        #    message.server.id) + '\n-------------------------')
        client.change_status(game=None)

        enabled_plugins = await self.get_plugins()
        for plugin in enabled_plugins:
            self.loop.create_task(plugin._on_message(message, pfx))

        if message.content.startswith('-read<@92747043885314048>'):
            if message.author.id == ownr:
                await client.send_message(message.channel, 'Alex stop wasting time and get back to working on my APIs...')
            elif message.author.id == '92747043885314048':
                await client.send_message(message.channel,
                                          'Ace, I heard Alex bought this giant black dildo, wanna go test it out?')
            else:
                await client.send_message(message.channel, 'No! ಠ_ಠ')


        elif message.content.startswith('(╯°□°）╯︵ ┻━┻'):
            await client.send_message(message.channel, '┬─┬﻿ ノ( ゜-゜ノ)')

        elif message.content.startswith(pfx + 'checkbullet'):
            cmd_name = 'PushBullet Message Check'
            await client.send_typing(message.channel)
            pushes = pb.get_pushes(limit=1)
            title = pushes[0]['title']
            body = pushes[0]['body']
            await client.send_message(message.channel, 'Title: `' + title + '`\nMessage: `' + body + '`')
            pb.dismiss_push(pushes[0]['iden'])
            #print('CMD [' + cmd_name + '] > ' + initiator_data)
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
            #print('CMD [' + cmd_name + '] > ' + initiator_data)


client = sigma()
client.run(token)