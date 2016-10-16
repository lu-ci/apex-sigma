import datetime
import os
import sys
import time
import discord
import logging
import json

from config import StartupType, dsc_email, dsc_password, sigma_version
from config import Token as token
from config import Prefix as pfx

from plugin_manager import PluginManager
from database import Database

print('Starting up...')
start_time = time.time()
time = time.time()
current_time = datetime.datetime.now().time()
current_time.isoformat()

if not os.path.isfile('config.py'):
    sys.exit(
        'Fatal Error: config.py is not present.\nIf you didn\'t already, rename config_example.py to config.py, fill out your credentials and try again.')
else:
    print('config.py present, continuing...')
# Data


# I love spaghetti!
class Sigma(discord.Client):
    def __init__(self):
        super().__init__()
        self.prefix = pfx

        self.init_logger()
        self.init_databases()
        self.init_plugins()

        self.server_count = 0
        self.member_count = 0

        with open('AUTHORS') as authors_file:
            content = json.load(authors_file)
            self.authors = content['authors']
            self.contributors = content['contributors']

    def init_logger(self):
        logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        self.log = logger

    def init_databases(self):
        self.db = Database('storage/server_settings.sqlite')

    def init_plugins(self):
        self.plugin_manager = PluginManager(self)
        self.plugin_manager.load_all()

    async def on_voice_state_update(self, before, after):
        enabled_plugins = await self.get_plugins()
        for plugin in enabled_plugins:
            self.loop.create_task(plugin._on_voice_state_update(before, after))

    async def get_plugins(self):
        plugins = await self.plugin_manager.get_all()
        return plugins

    async def on_ready(self):
        gamename = pfx + 'help'
        game = discord.Game(name=gamename)
        await client.change_presence(game=game)

        for server in client.servers:
            self.server_count += 1
            for member in server.members:
                self.member_count += 1

        print('-----------------------------------')
        print('Logged In As: ' + client.user.name)
        print('Bot User ID: ' + client.user.id)
        print('Running discord.py version: ' + discord.__version__)
        print('Authors: {:s}'.format(', '.join(self.authors)))
        print('Contributors: {:s}'.format(', '.join(self.contributors)))
        print('Bot Version: ' + sigma_version)
        print('Build Date: 16. October 2016.')
        print('-----------------------------------')
        print('Connected to [ ' + str(self.server_count) + ' ] servers.')
        print('Serving [ ' + str(self.member_count) + ' ] users.')
        print('\nSuccessfully connected to Discord!')
        folder = 'cache/ow'
        try:
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)
        except FileNotFoundError:
            pass

        if not os.path.exists('cache/lol/'):
            os.makedirs('cache/lol/')
        if not os.path.exists('cache/ow/'):
            os.makedirs('cache/ow/')
        if not os.path.exists('cache/rip/'):
            os.makedirs('cache/rip/')
        if not os.path.exists('cache/ani/'):
            os.makedirs('cache/ani/')

    async def on_message(self, message):
        # Static Strings
        # initiator_data = ('by: ' + str(message.author) + '\nUserID: ' + str(message.author.id) + '\nContent: [' + str(
        #    message.content) + ']\nServer: ' + str(message.server.name) + '\nServerID: ' + str(
        #    message.server.id) + '\n-------------------------')
        client.change_presence()

        enabled_plugins = await self.get_plugins()

        for plugin in enabled_plugins:
            self.loop.create_task(plugin._on_message(message, pfx))


client = Sigma()
if StartupType == '0':
    if token == '':
        sys.exit('Token not provided, please open config.py and place your token.')
    else:
        pass
    try:
        client.run(token)
    except Exception as err:
        print(err)
elif StartupType == '1':
    if dsc_email == '' or dsc_password == '':
        sys.exit('Discord Email and/or Passoword not provided, please open config.py and fill in those details.')
    else:
        pass
    try:
        client.run(dsc_email, dsc_password)
    except Exception as err:
        print(err)
else:
    print('Failed loading connection settings.\nCheck your StartupType and make sure it\'s either 0 or 1.')
    sys.exit('Startup Type is not found.')
