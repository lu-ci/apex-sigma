import os
from importlib import import_module

from .permission import check_channel_nsfw
from sigma.core.formatting import code, codeblock


class EventNotEnabled(RuntimeError):
    pass


class Event(object):
    def __init__(self, plugin, info):
        self.enabled = False
        self.glob = False
        self.sfw = True
        self.usage = 'No usage available'
        self.desc = 'No description available'

        self.db = plugin.db
        self.log = plugin.log
        self.bot = plugin.bot
        self.plugin = plugin

        try:
            self.load_info(info)
        except EventNotEnabled:
            return

    def load_info(self, info):
        if 'enabled' not in info or not info['enabled']:
            raise EventNotEnabled
        else:
            self.enabled = True

        self.name = info['name']
        self.path = self.plugin.path

        self.type = info['type']

        if 'global' in info and info['global']:
            self.glob = True

        if 'usage' in info:
            self.usage = info['usage']

        if 'description' in info:
            self.desc = info['description']

        self.sfw = info['sfw']

        module_path = os.path.join(self.path, self.name)
        self.modpath = module_path.replace('/', '.')
        self.module = import_module(self.modpath)

    def help(self):
        usage = self.usage
        return 'Usage: {:s}\n{:s}'.format(
                code(usage), codeblock(self.desc))

    async def call(self, message, *args):
        channel = message.channel

        async def typing():
            await self.bot.send_typing(channel)

        async def reply(text):
            await typing()
            return await self.bot.send_message(channel, text)

        self.typing = typing
        self.reply = reply

        if not self.sfw and not check_channel_nsfw(self.db, channel.id):
            msg = 'Channel does not have NSFW permissions set, sorry.'
            await self.reply(msg)
            return

        await getattr(self.module, self.name)(self, message, *args)
