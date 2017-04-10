import discord
import yaml
import os
from config import Prefix


async def commands(cmd, message, args):
    if not args:
        embed = discord.Embed(color=0x696969, title='🔍 Please Enter a Module Group Name')
        embed.set_footer(text='Module groups can be seen with the ' + Prefix + 'modules command.')
        await message.channel.send(None, embed=embed)
        return
    module_group = ' '.join(args)
    directory = 'sigma/plugins'
    command_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'plugin.yml':
                file_path = (os.path.join(root, file))
                with open(file_path) as plugin_file:
                    plugin_data = yaml.safe_load(plugin_file)
                    category = plugin_data['categories'][0]
                    if category == module_group.lower():
                        if plugin_data['enabled']:
                            try:
                                for command in sorted(plugin_data['commands'], key=lambda x: x['name']):
                                    plugin_name = command['name']
                                    command_list.append(Prefix + plugin_name)
                            except:
                                pass
    if len(command_list) == 0:
        embed = discord.Embed(color=0x696969, title='🔍 Module Group Not Found')
        await message.channel.send(None, embed=embed)
        return
    embed_to_user = discord.Embed(color=0x1abc9c)
    embed_to_user.add_field(name='Sigma\'s Commands In ' + module_group.title(),
                            value='```yaml\n' + ', '.join(command_list) + '\n```')
    await cmd.bot.send_message(message.author, None, embed=embed_to_user)
    if message.guild:
        embed_local = discord.Embed(color=0x66CC66, title='✅ List Sent To Your DM')
        await message.channel.send(None, embed=embed_local)
