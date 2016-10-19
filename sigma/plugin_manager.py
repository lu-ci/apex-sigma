<<<<<<< HEAD:plugin_manager.py
from plugin import Plugin
=======
from .plugin import Plugin
from .utils import create_logger
from . import plugins as plug
>>>>>>> dev:sigma/plugin_manager.py

# * imports are ugly but it works
from plugins import *


class PluginManager:
    def __init__(self, client):
        self.client = client
        self.client.plugins = []

    def load(self, plugin):
<<<<<<< HEAD:plugin_manager.py
        print('Plugin Manager: Loading Plugin: [ ' + plugin.__name__ + ' ]')
        plugin_instance = plugin(self.client)
        self.client.plugins.append(plugin_instance)
=======
        plugname = plugin.__name__

        if plugname in plug.pluglist:
            self.log.info('Loading Plugin: [ {:s} ]'.format(plugname))
            plugin_instance = plugin(self.client)
            self.client.plugins.append(plugin_instance)
>>>>>>> dev:sigma/plugin_manager.py

    def load_all(self):
        n = 0
        print('\nPlugin Manager: Starting Mass Plugin Load\n')
        for plugin in Plugin.plugins:
            self.load(plugin)
            n += 1
        print('\nFinished Mass Plugin Load\nTotal Plugins Loaded: ' + str(n) + '\n')

    async def get_all(self):
        plugins = []
        for plugin in self.client.plugins:
            if plugin.is_global:
                plugins.append(plugin)
                # if plugin.__class__.__name__ in plugin_names:
                #    plugins.append(plugin)
        return plugins
