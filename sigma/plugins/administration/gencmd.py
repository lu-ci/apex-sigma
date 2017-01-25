import os
import yaml
from config import DevMode


async def gencmd(ev):
    if DevMode:
        ev.log.info('Generating Command List...')
        directory = 'sigma/plugins'

        out_text = '#Sigma\'s List of Commands'
        n = 0
        category_curr = 'None'
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file == 'plugin.yml':
                    file_path = (os.path.join(root, file))
                    with open(file_path) as plugin_file:
                        plugin_data = yaml.load(plugin_file)
                        try:
                            category = plugin_data['categories'][0]
                        except:
                            pass
                        try:
                            if category != 'administration':
                                if plugin_data['enabled']:
                                    for command in plugin_data['commands']:
                                        plugin_name = command['name']
                                        try:
                                            plugin_usage = command['usage'].replace('{pfx:s}', '>>').replace('{cmd:s}', plugin_name)
                                        except:
                                            plugin_usage = '>>' + plugin_name
                                        plugin_desc = command['description']
                                        if category == category_curr:
                                            pass
                                        else:
                                            category_curr = category
                                            out_text += '\n###' + category.upper()
                                            out_text += '\nCommand |  Description |  Usage'
                                            out_text += '\n--------|--------------|-------'
                                        out_text += '\n`>>' + plugin_name + '`  |  ' + plugin_desc + '  |  `' + plugin_usage + '`'
                                        n += 1
                        except:
                            pass
                        with open("COMMANDLIST.md", "w") as text_file:
                            text_file.write(out_text)
        ev.log.info('Command List Generated Successfully With ' + str(n) + ' Commands.')

