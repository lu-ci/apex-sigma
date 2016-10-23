import os
import datetime
import time
import discord
import yaml

from config import Prefix as pfx
from config import sigma_version

from .plugman import PluginManager
from .database import Database
from .logger import create_logger


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
            content = yaml.load(authors_file)
            self.authors = content['authors']
            self.contributors = content['contributors']
        with open('DONORS') as donors_file:
            content = yaml.load(donors_file)
            self.donors = content['donors']

    def run(self, token):
        self.log.info('Starting up...')
        self.start_time = time.time()
        self.time = time.time()
        current_time = datetime.datetime.now().time()
        current_time.isoformat()

        super().run(token)

    def init_logger(self):
        self.log = create_logger('Sigma')

    def init_databases(self):
        db_path = 'db/server_settings.sqlite'
        sql_file = 'db/server_settings.sql'
        self.db = Database(db_path, sql_file)

    def init_plugins(self):
        self.plugin_manager = PluginManager(self)

    def create_cache(self):
        if not os.path.exists('cache/lol/'):
            os.makedirs('cache/lol/')
        if not os.path.exists('cache/ow/'):
            os.makedirs('cache/ow/')
        if not os.path.exists('cache/rip/'):
            os.makedirs('cache/rip/')
        if not os.path.exists('cache/ani/'):
            os.makedirs('cache/ani/')

        folder = 'cache/ow'

        try:
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    self.log.error(e)
        except FileNotFoundError:
            pass

    async def on_voice_state_update(self, before, after):
        pass

    async def get_plugins(self):
        return self.plugin_manager.plugins

    async def on_ready(self):
        self.log.info('Checking API Keys...')
        gamename = self.prefix + 'help'
        game = discord.Game(name=gamename)
        await self.change_presence(game=game)
        self.create_cache()
        for server in self.servers:
            self.server_count += 1
            for member in server.members:
                self.member_count += 1

        self.log.info('-----------------------------------')
        self.log.info('Logged In As: ' + self.user.name)
        self.log.info('Bot User ID: ' + self.user.id)
        self.log.info('Running discord.py version: ' + discord.__version__)
        self.log.info('Authors: {:s}'.format(', '.join(self.authors)))
        self.log.info('Contributors: {:s}'.format(', '.join(self.contributors)))
        self.log.info('Donors: {:s}'.format(', '.join(self.donors)))
        self.log.info('Bot Version: ' + sigma_version)
        self.log.info('Build Date: 16. October 2016.')
        self.log.info('-----------------------------------')
        self.log.info('Connected to [ {:d} ] servers'.format(self.server_count))
        self.log.info('Serving [ {:d} ] users'.format(self.member_count))
        self.log.info('Successfully connected to Discord!')

    async def on_message(self, message):
        self.change_presence()

        args = message.content.split(' ')

        # handle mention events
        if self.user.mentioned_in(message):
            for ev_name, event in self.plugin_manager.events['mention'].items():
                await event.call(message, args)

        # handle raw message events
        for ev_name, event in self.plugin_manager.events['message'].items():
            await event.call(message, args)

        if message.content.startswith(pfx):
            cmd = args.pop(0).lstrip(pfx)

            try:
                task = self.plugin_manager.commands[cmd].call(message, args)
                self.loop.create_task(task)

                if message.server:
                    msg = 'User %s [%s] on server %s [%s], used the {:s} command on #%s channel'
                    self.log.info(msg.format(cmd),
                                  message.author, message.author.id,
                                  message.server.name, message.server.id, message.channel)
                else:
                    msg = 'User %s [%s], used the command.'
                    self.log.info(msg.format(cmd),
                                  message.author,
                                  message.author.id)
            except KeyError:
                # no such command
                pass
