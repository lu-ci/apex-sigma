import os
import datetime
import time
import discord
import yaml

from config import Prefix as pfx

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
        db_addr = db_url or 'mongodb://localhost:27017'
        self.db = Database(db_addr)

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

    def make_stats(self):
        check_res = self.db.find('Stats', {'Role': 'Stats'})
        n = 0
        for res in check_res:
            n += 1
        if n == 0:
            stats_data_full = {
                'Role': 'Stats',
                'ServerCount': self.server_count,
                'UserCount': self.member_count,
            }
            self.db.insert_one('Stats', stats_data_full)
        else:
            stats_data_update = {
                'ServerCount': self.server_count,
                'UserCount': self.member_count,
            }
            updatetarget = {"Role": 'Stats'}
            updatedata = {"$set": stats_data_update}
            self.db.update_one('Stats', updatetarget, updatedata)

    def make_server_list(self):
        for server in self.servers:
            member_count = 0
            bot_count = 0
            srch_data = {
                'ServerID': server.id
            }
            serv_found = 0
            search = self.db.find('Servers', srch_data)
            for res in search:
                serv_found += 1
            for member in server.members:
                if member.bot:
                    bot_count += 1
                else:
                    member_count += 1
            if serv_found == 0:
                data = {
                    'ServerID': server.id,
                    'ServerName': server.name,
                    'Created': server.created_at,
                    'DefaultChannelID': server.default_channel.id,
                    'DefaultChannelName': server.default_channel.name,
                    'MemberCount': member_count,
                    'BotCount': bot_count,
                    'Owner': server.owner.name,
                    'OwnerID': server.owner_id,
                    'Region': str(server.region),
                    'SecLevel': str(server.verification_level),
                    'MFALevel': str(server.mfa_level)
                }
                self.db.insert_one('Servers', data)
            else:
                updatedata = {
                    'ServerName': server.name,
                    'DefaultChannelID': server.default_channel.id,
                    'DefaultChannelName': server.default_channel.name,
                    'MemberCount': member_count,
                    'BotCount': bot_count,
                    'Owner': server.owner.name,
                    'OwnerID': server.owner_id,
                    'Region': str(server.region),
                    'SecLevel': str(server.verification_level),
                    'MFALevel': str(server.mfa_level)
                }
                updatetarget = {"ServerID": server.id}
                updatedata = {"$set": updatedata}
                self.db.update_one('Stats', updatetarget, updatedata)

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
        self.log.info('-----------------------------------')
        self.make_stats()
        self.log.info('Updated Stats')
        self.make_server_list()
        self.log.info('Updated Server List')
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
