import discord
from config import Prefix


async def commands(cmd, message, args):
    if not args:
        embed = discord.Embed(color=0x696969, title='🔍 Please Enter a Module Group Name')
        embed.set_footer(text='Module groups can be seen with the ' + Prefix + 'modules command.')
        await message.channel.send(None, embed=embed)
        return
    module_group = ' '.join(args).lower()
    command_list = []
    all_commands = cmd.bot.plugin_manager.commands
    for command in all_commands:
        if module_group in all_commands[command].plugin.categories:
            command_list.append(f'{Prefix}{command}')
    if len(command_list) == 0:
        embed = discord.Embed(color=0x696969, title='🔍 Module Group Not Found')
        await message.channel.send(None, embed=embed)
        return
    embed_to_user = discord.Embed(color=0x1abc9c)
    embed_to_user.add_field(name='Sigma\'s Commands In ' + module_group.title(),
                            value='```yaml\n' + ', '.join(command_list) + '\n```')
    await message.author.send(None, embed=embed_to_user)
    if message.guild:
        embed_local = discord.Embed(color=0x66CC66, title='✅ List Sent To Your DM')
        await message.channel.send(None, embed=embed_local)
