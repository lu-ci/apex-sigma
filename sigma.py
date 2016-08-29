# noinspection PyPep8
import datetime
import os
import sys
import time
import discord
import logging
import random

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

print('Starting up...')
start_time = time.time()
time = time.time()
current_time = datetime.datetime.now().time()
current_time.isoformat()

if not os.path.isfile('config.py'):
    sys.exit(
        'Fatal Error: config.py is not present.\nIf you didn\'t already, rename config.example.json to config.json and try again.')
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
from plugins.rip import Rip
from plugins.lastfm import LastFM
from plugins.cleverbot import Cleverbot
from plugins.echo import Echo

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

        if not os.path.exists('cache/lol/'):
            os.makedirs('cache/lol/')
        if not os.path.exists('cache/ow/'):
            os.makedirs('cache/ow/')
        if not os.path.exists('cache/rip/'):
            os.makedirs('cache/rip/')

    async def on_message(self, message):
        # Static Strings
        #initiator_data = ('by: ' + str(message.author) + '\nUserID: ' + str(message.author.id) + '\nContent: [' + str(
        #    message.content) + ']\nServer: ' + str(message.server.name) + '\nServerID: ' + str(
        #    message.server.id) + '\n-------------------------')
        client.change_status(game=None)

        enabled_plugins = await self.get_plugins()
        for plugin in enabled_plugins:
            self.loop.create_task(plugin._on_message(message, pfx))



        if message.content.startswith('(╯°□°）╯︵ ┻━┻'):
            table = ['┬─┬ ノ( ^_^ノ)',
            '┬─┬ ﾉ(° -°ﾉ)',
            '┬─┬ ノ(゜-゜ノ)',
            '┬─┬ ノ(ಠ\_ಠノ)',
            '┻━┻~~~~  ╯(°□° ╯)',
            '┻━┻====  ╯(°□° ╯)']
            logger.info("Table fliped by %s [%s], unflipping", message.author, message.author.id)
            await client.send_message(message.channel, random.choice(table))

client = sigma()
client.run(token)