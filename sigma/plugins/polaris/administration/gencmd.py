import os
import yaml
from config import Prefix, permitted_id


async def gencmd(cmd, message, args):
    if message.author.id in permitted_id:
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
                            for command in plugin_data['commands']:
                                plugin_name = command['name']
                                plugin_usage = command['usage'].replace('{pfx:s}', '>>').replace('{cmd:s}',
                                                                                                   plugin_name)
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
        await cmd.bot.send_message(message.channel, 'Commands Exported: ' + str(n))
