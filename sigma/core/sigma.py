import os
import datetime
import arrow
import discord
import yaml
import aiohttp

from config import Prefix, MongoAddress, MongoPort, MongoAuth, MongoUser, MongoPass, DiscordListToken, DevMode
from config import UseCachet, CachetToken, CachetURL
from .utils import load_module_list
from .plugman import PluginManager
from .database import Database
from .music import Music
from .logger import create_logger
from .stats import stats
from .command_alts import load_alternate_command_names
from .blacklist import check_black
from .blacklist import check_perms
from .cooldowns import Cooldown


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
class Sigma(discord.AutoShardedClient):
    def __init__(self):
        super().__init__()
        self.prefix = Prefix
        self.alts = load_alternate_command_names()
        self.module_list = load_module_list()
        self.init_logger()
        self.init_databases()
        self.init_music()
        self.init_cooldown()
        self.init_plugins()
        self.ready = False
        self.guild_count = 0
        self.member_count = 0
        self.command_count = 0
        self.message_count = 0

        with open('AUTHORS') as authors_file:
            content = yaml.safe_load(authors_file)
            self.authors = content['authors']
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
        self.start_time = arrow.utcnow().timestamp
        current_time = datetime.datetime.now().time()
        current_time.isoformat()
        self.log.info('Sending Client Startup Signal...')
        super().run(token)

    def init_logger(self):
        self.log = create_logger('Sigma')

    async def update_discordlist(self):
        if not DevMode:
            payload = {
                "token": DiscordListToken,
                "servers": len(self.guilds)
            }
            url = "https://bots.discordlist.net/api.php"
            async with aiohttp.ClientSession() as session:
                conn = await session.post(url, data=payload)
                await conn.release()

    async def cachet_stat_up(self, metric_id, value):
        try:
            headers = {'X-Cachet-Token': CachetToken}
            payload = {'value': value}
            url = f"{CachetURL}api/v1/metrics/{metric_id}/points"
            async with aiohttp.ClientSession() as session:
                conn = await session.post(url, data=payload, headers=headers)
                await conn.release()
        except Exception as e:
            self.log.error(f'STAT UPDATE FAIL: {e}')

    def init_databases(self):
        self.db = Database(MongoAddress, MongoPort, MongoAuth, MongoUser, MongoPass)

    def init_plugins(self):
        self.plugin_manager = PluginManager(self)

    def init_music(self):
        self.music = Music()

    def init_cooldown(self):
        self.cooldown = Cooldown()

    @classmethod
    def create_cache(cls):
        if not os.path.exists('cache/'):
            os.makedirs('cache/')
        if not os.path.exists('chains/'):
            os.makedirs('chains/')

    async def get_plugins(self):
        return self.plugin_manager.plugins

    async def on_ready(self):
        self.log.info('Connecting To Database')
        self.db.init_stats_table()
        self.log.info('Making Cache')
        self.create_cache()
        self.log.info('-----------------------------------')
        stats(self, self.log)
        self.db.init_server_settings(self.guilds)
        self.log.info('-----------------------------------')
        self.log.info('Updating Bot Population Stats...')
        self.db.update_population_stats(self.guilds, self.get_all_members())
        self.log.info('Starting UserList Refactor Node')
        self.loop.create_task(self.db.refactor_users(self.get_all_members()))
        self.log.info('Starting ServerList Refactor Node')
        self.loop.create_task(self.db.refactor_servers(self.guilds))
        self.log.info('Updating Bot Listing APIs...')
        self.loop.create_task(self.update_discordlist())
        self.log.info('Launching On-Ready Plugins...')
        for ev_name, event in self.plugin_manager.events['ready'].items():
            try:
                task = event.call_ready()
                self.loop.create_task(task)
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
            self.message_count += 1
            args = message.content.split(' ')
            # handle mention events
            if type(message.author) == discord.Member:
                black = check_black(self.db, message)
            else:
                black = False
            if self.user.mentioned_in(message):
                if not black:
                    for ev_name, event in self.plugin_manager.events['mention'].items():
                        task = event.call(message, args)
                        self.loop.create_task(task)
            # handle raw message events
            if not black:
                for ev_name, event in self.plugin_manager.events['message'].items():
                    task = event.call(message, args)
                    self.loop.create_task(task)

            if message.content.startswith(Prefix):
                cmd = args.pop(0).lstrip(Prefix).lower()
                if cmd in self.alts:
                    cmd = self.alts[cmd]
                try:
                    permed = check_perms(self.db, message, self.plugin_manager.commands[cmd])
                    if not black and permed:
                        task = self.plugin_manager.commands[cmd].call(message, args)
                        self.loop.create_task(task)
                        self.db.add_stats(f'cmd_{cmd}_count')
                        self.db.add_stats('CMDCount')
                        self.command_count += 1
                        if UseCachet:
                            self.loop.create_task(self.cachet_stat_up(1, 1))
                    athr = message.author
                    msg = f'CMD: {cmd} | USR: {athr.name}#{athr.discriminator} [{athr.id}]'
                    if message.guild:
                        msg += f' | SRV: {message.guild.name} [{message.guild.id}]'
                        msg += f' | CHN: #{message.channel.name} [{message.channel.id}]'
                        if args:
                            msg = f'{msg} | ARGS: {" ".join(args)}'

                    else:
                        msg += f' | PRIVATE MESSAGE'
                        if args:
                            msg += f' | ARGS: {" ".join(args)}'
                    self.log.info(msg)
                except KeyError:
                    # no such command
                    pass

    async def on_member_join(self, member):
        if self.ready:
            self.db.update_population_stats(self.guilds, self.get_all_members())
            for ev_name, event in self.plugin_manager.events['member_join'].items():
                task = event.call_sp(member)
                self.loop.create_task(task)

    async def on_member_remove(self, member):
        if self.ready:
            self.db.update_population_stats(self.guilds, self.get_all_members())
            for ev_name, event in self.plugin_manager.events['member_leave'].items():
                task = event.call_sp(member)
                self.loop.create_task(task)

    async def on_guild_join(self, server):
        await self.update_discordlist()
        self.db.add_new_server_settings(server)
        self.db.update_server_details(server)
        self.db.update_population_stats(self.guilds, self.get_all_members())
        msg = f'INV | SRV: {server.name} [{server.id}] | OWN: {server.owner.name} [{server.owner.id}]'
        self.log.info(msg)
        self.db.init_server_settings(self.guilds)
        if UseCachet:
            self.loop.create_task(self.cachet_stat_up(3, 1))

    async def on_guild_remove(self, server):
        await self.update_discordlist()
        self.db.update_population_stats(self.guilds, self.get_all_members())
        msg = f'RMV | SRV: {server.name} [{server.id}] | OWN: {server.owner.name} [{server.owner.id}]'
        self.log.info(msg)
        if UseCachet:
            self.loop.create_task(self.cachet_stat_up(3, -1))

    async def on_member_update(self, before, after):
        if self.ready:
            self.db.update_user_details(after)

    async def on_guild_update(self, before, after):
        if self.ready:
            self.db.update_server_details(after)
