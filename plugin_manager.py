from plugin import Plugin

# * imports are ugly but it works
from plugins import *


class PluginManager:
    def __init__(self, client):
        self.client = client
        self.client.plugins = []

    def load(self, plugin):
        print('Plugin Manager: Loading Plugin: [ ' + plugin.__name__ + ' ]')
        plugin_instance = plugin(self.client)
        self.client.plugins.append(plugin_instance)

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
