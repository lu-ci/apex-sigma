import os
import datetime
import time
import discord
import yaml

from config import Prefix as pfx, MongoAddress, MongoPort

from .plugman import PluginManager
from .database import Database
from .logger import create_logger
from .stats import stats


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
        db_url = os.getenv('DATABASE_URL')
        db_addr = db_url or 'mongodb://' + MongoAddress + ':' + str(MongoPort)
        self.db = Database(db_addr)

    def init_plugins(self):
        self.plugin_manager = PluginManager(self)

    def create_cache(self):
        if not os.path.exists('cache/'):
            os.makedirs('cache/')

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
        stats(self, self.log)
        servers = []
        for srv in self.servers:
            servers.append(srv)
        self.db.init_server_settings(servers)
        user_generator = self.get_all_members()
        self.db.refactor_users(user_generator)
        self.db.refactor_servers(servers)
        self.log.info('-----------------------------------')
        self.log.info('Successfully connected to Discord!')

    async def on_message(self, message):
        self.db.update_user_details(message.author)
        if message.server:
            self.db.update_server_details(message.server)
        self.change_presence()
        self.db.add_stats('MSGCount')
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
                    msg = 'User %s [%s], used the {:s} command in a private message channel.'
                    self.log.info(msg.format(cmd),
                                  message.author,
                                  message.author.id)
            except KeyError:
                # no such command
                pass

    async def on_member_join(self, member):
        for ev_name, event in self.plugin_manager.events['member_join'].items():
            await event.call_sp(member)

    async def on_member_remove(self, member):
        for ev_name, event in self.plugin_manager.events['member_leave'].items():
            await event.call_sp(member)

    async def on_server_join(self, server):
        self.db.add_new_server_settings(server)
        self.db.update_user_details(server)
        self.log.info('New Server Added: ' + server.name)
