import discord
import yaml
import os


async def modules(cmd, message, args):
    directory = 'sigma/plugins'
    module_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'plugin.yml':
                file_path = (os.path.join(root, file))
                with open(file_path) as plugin_file:
                    plugin_data = yaml.safe_load(plugin_file)
                    try:
                        category = plugin_data['categories'][0]
                        if category.title() not in module_list and category not in ['administration', 'special']:
                            module_list.append(category.title())
                    except:
                        pass
    embed_to_user = discord.Embed(color=0x1abc9c)
    embed_to_user.add_field(name='🔍 Sigma\'s Module Group List', value='```yaml\n' + '\n'.join(module_list) + '\n```')
    await cmd.bot.send_message(message.author, None, embed=embed_to_user)
    if message.guild:
        embed_local = discord.Embed(color=0x66CC66, title='✅ List Sent To Your DM')
        await message.channel.send(None, embed=embed_local)
