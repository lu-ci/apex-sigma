from .plugin import Plugin
from .utils import create_logger
from . import plugins as plug


class PluginManager(object):
    def __init__(self, client):
        self.log = create_logger('pluginmanager')
        self.client = client
        self.client.plugins = []

    def load(self, plugin):
        plugname = plugin.__name__

        if plugname in plug.pluglist:
            self.log.info('Loading Plugin: [ {:s} ]'.format(plugname))
            plugin_instance = plugin(self.client)
            self.client.plugins.append(plugin_instance)

    def load_all(self):
        self.log.info('Starting Mass Plugin Load')

        for plugin in Plugin.plugins:
            self.load(plugin)

        self.log.info('Finished Mass Plugin Load')
        self.log.info('Total Plugins Loaded: {:d}'.format(len(self.client.plugins)))

    async def get_all(self):
        plugins = []

        for plugin in self.client.plugins:
            if plugin.is_global:
                plugins.append(plugin)

        return plugins
