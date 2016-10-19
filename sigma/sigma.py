import sys
import os
import datetime
import time
import discord
import logging
<<<<<<< HEAD:sigma.py
=======
import json
import sqlite3
>>>>>>> dev:sigma/sigma.py

from config import Prefix as pfx
from config import sigma_version

from .plugin_manager import PluginManager
from .database import Database


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

if token == '':
    sys.exit('Token not provided, please open config.py and place your token.')


# I love spaghetti!
class Sigma(discord.Client):
    def __init__(self):
        super().__init__()
        self.prefix = pfx

        # self.init_logger()
        self.init_databases()
        self.init_plugins()

    def init_logger(self):
        logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        self.log = logger

    def init_databases(self):
        db_path = 'db/server_settings.sqlite'
        if os.path.isfile(db_path):
            pass
        else:
            print('Database Not Found')
            open(db_path, 'w+')
        db_conn = sqlite3.connect(db_path)
        db_intructions = open('db/server_settings.sql', 'r').read()
        cur = db_conn.cursor()
        cur.executescript(db_intructions)
        db_conn.commit()
        cur.close()
        db_conn.close()
        self.db = Database(db_path)

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
        await self.change_presence(game=game)

<<<<<<< HEAD:sigma.py
        server_amo = 0
        member_amo = 0
        for server in client.servers:
            server_amo += 1
=======
        for server in self.servers:
            self.server_count += 1
>>>>>>> dev:sigma/sigma.py
            for member in server.members:
                member_amo += 1

        print('-----------------------------------')
        print('Logged In As: ' + self.user.name)
        print('Bot User ID: ' + self.user.id)
        print('Running discord.py version: ' + discord.__version__)
        print('Authors: AXAz0r, Awakening')
        print('Contributors: Mirai, Chaeldar, Valeth')
        print('Bot Version: ' + sigma_version)
        print('Build Date: 05. October 2016.')
        print('-----------------------------------')
        print('Connected to [ ' + str(server_amo) + ' ] servers.')
        print('Serving [ ' + str(member_amo) + ' ] users.')
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
        self.change_presence()

        enabled_plugins = await self.get_plugins()

        for plugin in enabled_plugins:
            self.loop.create_task(plugin._on_message(message, pfx))
<<<<<<< HEAD:sigma.py


client = Sigma()
if StartupType == '0':
    try:
        client.run(token)
    except Exception as err:
        print(err)
elif StartupType == '1':
    try:
        client.run(dsc_email, dsc_password)
    except Exception as err:
        print(err)
else:
    print('Failed loading connection settings.\nCheck your StartupType and make sure it\'s either 0 or 1.')
    sys.exit('Startup Type is not found.')
=======
>>>>>>> dev:sigma/sigma.py
