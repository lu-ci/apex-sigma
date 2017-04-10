import discord


async def listselfroles(cmd, message, args):
    self_roles = cmd.db.get_settings(message.guild.id, 'SelfRoles')
    role_list = ''
    for role in self_roles:
        role_list += '\n - ' + role
    if role_list == '':
        embed = discord.Embed(type='rich', color=0x0099FF,
                              title='ℹ No Self Assignable Roles Set')
    else:
        embed = discord.Embed(color=0x1ABC9C)
        embed.add_field(name='Self Assignable Roles On ' + message.guild.name, value='```\n' + role_list + '\n```')
    await message.channel.send(None, embed=embed)
