import os
from importlib import import_module

from .permission import check_channel_nsfw


class NotEnabledError(RuntimeError):
    pass


class Callable(object):
    def __init__(self, plugin, info):
        self.enabled = False
        self.glob = False
        self.sfw = True
        self.usage = 'No usage info available.'
        self.desc = 'No description available.'

        self.db = plugin.db
        self.log = plugin.log
        self.bot = plugin.bot
        self.plugin = plugin

        try:
            self.load_info(info)
        except NotEnabledError:
            return

    def load_info(self, info):
        if 'enabled' not in info or not info['enabled']:
            raise NotEnabledError
        else:
            self.enabled = True

        self.name = info['name']
        self.path = self.plugin.path

        if 'global' in info and info['global']:
            self.glob = True

        if 'usage' in info:
            self.usage = info['usage']

        if 'description' in info:
            self.desc = info['description']

        self.sfw = info['sfw']

        module_path = os.path.join(self.path, self.name)
        self.modpath = module_path.replace('/', '.').replace('\\', '.')
        self.module = import_module(self.modpath)

    def resource(self, path):
        return os.path.join(self.path, 'res', path)

    def help(self):
        return ''

    async def call(self, message, *args):
        channel = message.channel
        msg = None

        if not self.sfw and not check_channel_nsfw(self.db, channel.id):
            msg = 'Channel does not have NSFW permissions set, sorry.'
        else:
            msg = await getattr(self.module, self.name)(self, message, *args)

        if not self.sfw and check_channel_nsfw(self.db, channel.id):
            self.db.add_stats('NSFWCount')

        if msg:
            await self.bot.send_typing(channel)
            await self.bot.send_message(channel, msg)
