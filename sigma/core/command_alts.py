import os
import yaml


def load_alternate_command_names():
    alts = {}
    directory = 'sigma/plugins'
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'plugin.yml':
                file_path = (os.path.join(root, file))
                with open(file_path) as plugin_file:
                    plugin_data = yaml.safe_load(plugin_file)
                    if plugin_data['enabled']:
                        if 'commands' in plugin_data:
                            for command in plugin_data['commands']:
                                if 'alts' in command:
                                    for alt in command['alts']:
                                        plugin_name = command['name']
                                        alts.update({alt: plugin_name})
    return alts
