from plugin import Plugin

class PluginManager:

    def __init__(self, client):
        self.client = client
        self.client.plugins = []

    def load(self, plugin):
        print('Plugin manager: loading plugin ' + plugin.__name__)
        plugin_instance = plugin(self.client)
        self.client.plugins.append(plugin_instance)

    def load_all(self):
        print('\nPlugin manager: starting plugin load\n')
        for plugin in Plugin.plugins:
            self.load(plugin)

    async def get_all(self):
        plugins = []
        for plugin in self.client.plugins:
            if plugin.is_global:
                plugins.append(plugin)
            #if plugin.__class__.__name__ in plugin_names:
            #    plugins.append(plugin)
        return plugins
