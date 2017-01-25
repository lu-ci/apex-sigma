import os
import datetime
import time
import discord
import yaml
import aiohttp

from config import Prefix as pfx, MongoAddress, MongoPort, MongoAuth, MongoUser, MongoPass, DiscordListToken, DevMode

from .plugman import PluginManager
from .database import Database
from .logger import create_logger
from .stats import stats


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

    async def update_discordlist(self):
        if not DevMode:
            payload = {
                "token": DiscordListToken,
                "servers": len(self.servers)
            }
            url = "https://bots.discordlist.net/api.php"
            resp = await aiohttp.post(url, data=payload)
            resp.close()

    def init_databases(self):
        self.db = Database(MongoAddress, MongoPort, MongoAuth, MongoUser, MongoPass)

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
        self.db.init_stats_table()
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
        self.log.info('-----------------------------------')
        self.log.info('Updating User Database...')
        self.db.refactor_users(user_generator)
        self.log.info('Updating Server Database...')
        self.db.refactor_servers(servers)
        self.log.info('Updating Bot Population Stats...')
        self.db.update_population_stats(self.servers, self.get_all_members())
        self.log.info('Updating Bot Listing APIs...')
        await self.update_discordlist()
        self.log.info('Launching On-Ready Plguins...')
        for ev_name, event in self.plugin_manager.events['ready'].items():
            try:
                await event.call_ready()
            except Exception as e:
                self.log.error(e)
        self.log.info('-----------------------------------')
        self.log.info('Finished Loading Successfully Connected to Discord!')

    async def on_message(self, message):
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
            cmd = args.pop(0).lstrip(pfx).lower()

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
        self.db.update_user_details(member)
        self.db.update_population_stats(self.servers, self.get_all_members())
        for ev_name, event in self.plugin_manager.events['member_join'].items():
            try:
                await event.call_sp(member)
            except Exception as e:
                self.log.error(e)

    async def on_member_remove(self, member):
        self.db.update_population_stats(self.servers, self.get_all_members())
        for ev_name, event in self.plugin_manager.events['member_leave'].items():
            try:
                await event.call_sp(member)
            except Exception as e:
                self.log.error(e)

    async def on_server_join(self, server):
        await self.update_discordlist()
        self.db.add_new_server_settings(server)
        self.db.update_server_details(server)
        self.db.update_population_stats(self.servers, self.get_all_members())
        self.log.info('New Server Added: ' + server.name)

    async def on_member_update(self, member):
        self.db.update_user_details(member)

    async def on_server_update(self, server):
        self.db.update_server_details(server)
