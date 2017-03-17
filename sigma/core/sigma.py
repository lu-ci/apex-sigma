import os
import datetime
import arrow
import discord
import yaml
import aiohttp

from config import Prefix, MongoAddress, MongoPort, MongoAuth, MongoUser, MongoPass, DiscordListToken, DevMode

from .plugman import PluginManager
from .database import Database
from .music import Music
from .logger import create_logger
from .stats import stats
from .command_alts import load_alternate_command_names
from .blacklist import check_black


# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Aurora Project
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# I love spaghetti!
# Valebu pls, no take my spaghetti... :'(
class Sigma(discord.Client):
    def __init__(self):
        super().__init__()
        self.prefix = Prefix
        self.alts = load_alternate_command_names()
        self.init_logger()
        self.init_databases()
        self.init_music()
        self.init_plugins()
        self.ready = False
        self.server_count = 0
        self.member_count = 0

        with open('AUTHORS') as authors_file:
            content = yaml.safe_load(authors_file)
            self.authors = content['authors']
            self.contributors = content['contributors']
        with open('DONORS') as donors_file:
            content = yaml.safe_load(donors_file)
            self.donors = content['donors']
        with open('VERSION') as version_file:
            content = yaml.safe_load(version_file)
            version = content['version']
            self.build_date = datetime.datetime.fromtimestamp(content['build_date']).strftime('%B %d, %Y')
            self.v_major = version['major']
            self.v_minor = version['minor']
            self.v_patch = version['patch']
            self.codename = content['codename']
            self.beta_state = content['beta']

    def run(self, token):
        self.log.info('Starting up...')
        self.start_time = arrow.utcnow().timestamp
        current_time = datetime.datetime.now().time()
        current_time.isoformat()

        super().run(token)

    def init_logger(self):
        self.log = create_logger('Sigma')

    async def update_discordlist(self):
        if not DevMode:
            payload = {
                "token": DiscordListToken,
                "servers": len(self.servers)
            }
            url = "https://bots.discordlist.net/api.php"
            async with aiohttp.ClientSession() as session:
                session.post(url, data=payload)

    def init_databases(self):
        self.db = Database(MongoAddress, MongoPort, MongoAuth, MongoUser, MongoPass)

    def init_plugins(self):
        self.plugin_manager = PluginManager(self)

    def init_music(self):
        self.music = Music()

    async def missing_settings_check(self):
        self.log.info('Checking Missing Settings')
        check_count = 0
        for server in self.servers:
            self.db.check_for_missing_settings(server)
            check_count += 1
        self.log.info(f'Checked {check_count} Servers')
        self.log.info('Settings Check Complete')

    @classmethod
    def create_cache(cls):
        if not os.path.exists('cache/'):
            os.makedirs('cache/')

    async def on_voice_state_update(self, before, after):
        pass

    async def get_plugins(self):
        return self.plugin_manager.plugins

    async def on_ready(self):
        self.log.info('Connecting To Database')
        self.db.init_stats_table()
        self.log.info('Making Cache')
        self.create_cache()
        self.log.info('-----------------------------------')
        stats(self, self.log)
        self.db.init_server_settings(self.servers)
        self.log.info('-----------------------------------')
        self.log.info('Updating User Database...')
        self.loop.create_task(self.db.refactor_users(self.get_all_members()))
        self.log.info('Updating Server Database...')
        self.loop.create_task(self.db.refactor_servers(self.servers))
        self.log.info('Creating Loop To Check Database For Missing Settings')
        self.loop.create_task(self.missing_settings_check())
        self.log.info('-----------------------------------')
        self.log.info('Updating Bot Population Stats...')
        self.db.update_population_stats(self.servers, self.get_all_members())
        self.log.info('Updating Bot Listing APIs...')
        self.loop.create_task(self.update_discordlist())
        self.log.info('Launching On-Ready Plugins...')
        for ev_name, event in self.plugin_manager.events['ready'].items():
            try:
                await event.call_ready()
            except Exception as e:
                self.log.error(e)
        self.log.info('-----------------------------------')
        self.ready = True
        self.log.info('Finished Loading and Successfully Connected to Discord!')
        if os.getenv('DEV_BUILD_ENV'):
            self.log.info('Testing Build Environment Detected\nExiting...')
            exit()

    async def on_message(self, message):
        if self.ready:
            self.db.add_stats('MSGCount')
            args = message.content.split(' ')

            # handle mention events
            if self.user.mentioned_in(message):
                for ev_name, event in self.plugin_manager.events['mention'].items():
                    task = event.call(message, args)
                    self.loop.create_task(task)
            # handle raw message events
            for ev_name, event in self.plugin_manager.events['message'].items():
                task = event.call(message, args)
                self.loop.create_task(task)

            if message.content.startswith(Prefix):
                cmd = args.pop(0).lstrip(Prefix).lower()
                if cmd in self.alts:
                    cmd = self.alts[cmd]
                try:
                    if check_black(self.db, message):
                        self.log.warning('BLACK: Access Denied.')
                    else:
                        task = self.plugin_manager.commands[cmd].call(message, args)
                        self.loop.create_task(task)
                        self.db.add_stats(f'cmd_{cmd}_count')
                    if message.server:
                        if args:
                            msg = 'CMD: {:s} | USR: {:s} [{:s}] | SRV: {:s} [{:s}] | CHN: {:s} [{:s}] | ARGS: {:s}'
                            self.log.info(msg.format(cmd, message.author.name + '#' + message.author.discriminator,
                                                     message.author.id, message.server.name, message.server.id,
                                                     '#' + message.channel.name, message.channel.id, ' '.join(args)))
                        else:
                            msg = 'CMD: {:s} | USR: {:s} [{:s}] | SRV: {:s} [{:s}] | CHN: {:s} [{:s}]'
                            self.log.info(msg.format(cmd, message.author.name + '#' + message.author.discriminator,
                                                     message.author.id, message.server.name, message.server.id,
                                                     '#' + message.channel.name, message.channel.id))
                    else:
                        if args:
                            msg = 'CMD: {:s} | USR: {:s} [{:s}] | PRIVATE MESSAGE | ARGS: {:s}'
                            self.log.info(msg.format(cmd, message.author.name + '#' + message.author.discriminator,
                                                     message.author.id, ' '.join(args)))
                        else:
                            msg = 'CMD: {:s} | USR: {:s} [{:s}] | PRIVATE MESSAGE'
                            self.log.info(msg.format(cmd, message.author.name + '#' + message.author.discriminator,
                                                     message.author.id))
                except KeyError:
                    # no such command
                    pass

    async def on_member_join(self, member):
        if self.ready:
            self.db.update_population_stats(self.servers, self.get_all_members())
            for ev_name, event in self.plugin_manager.events['member_join'].items():
                task = event.call_sp(member)
                self.loop.create_task(task)

    async def on_member_remove(self, member):
        if self.ready:
            self.db.update_population_stats(self.servers, self.get_all_members())
            for ev_name, event in self.plugin_manager.events['member_leave'].items():
                task = event.call_sp(member)
                self.loop.create_task(task)

    async def on_server_join(self, server):
        await self.update_discordlist()
        self.db.add_new_server_settings(server)
        self.db.update_server_details(server)
        self.db.update_population_stats(self.servers, self.get_all_members())
        msg = 'INV | SRV: {:s} [{:s}] | OWN: {:s} [{:s}]'
        self.log.info(msg.format(server.name, server.id, server.owner.name, server.owner.id))
        self.db.init_server_settings(self.servers)

    async def on_server_remove(self, server):
        await self.update_discordlist()
        self.db.update_population_stats(self.servers, self.get_all_members())
        msg = 'RMV | SRV: {:s} [{:s}] | OWN: {:s} [{:s}]'
        self.log.info(msg.format(server.name, server.id, server.owner.name, server.owner.id))

    async def on_member_update(self, before, after):
        if self.ready:
            self.db.update_user_details(after)

    async def on_server_update(self, before, after):
        if self.ready:
            self.db.update_server_details(after)
