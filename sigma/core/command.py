import os
from importlib import import_module


class CommandNotEnabled(RuntimeError):
    pass


class Command(object):
    def __init__(self, plugin, info):
        self.enabled = False
        self.glob = False
        self.db = plugin.db
        self.log = plugin.log
        self.bot = plugin.bot
        self.plugin = plugin

        try:
            self.load_info(info)
        except CommandNotEnabled:
            return

    def load_info(self, info):
        if 'enabled' not in info or not info['enabled']:
            raise CommandNotEnabled
        else:
            self.enabled = True

        self.name = info['name']
        self.path = self.plugin.path

        if 'global' in info and info['global']:
            self.glob = True

        module_path = os.path.join(self.path, self.name)
        self.modpath = module_path.replace('/', '.')
        self.module = import_module(self.modpath)

    async def call(self, message, *args):
        await getattr(self.module, self.name)(self, message, *args)
