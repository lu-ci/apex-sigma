import discord


async def listselfroles(cmd, message, args):
    self_roles = cmd.db.get_settings(message.server.id, 'SelfRoles')
    role_list = ''
    for role in self_roles:
        role_list += '\n - ' + role
    if role_list == '':
        embed = discord.Embed(type='rich', color=0x0099FF,
                              title=':information_source: No Self Assignable Roles Set')
    else:
        embed = discord.Embed(color=0x1ABC9C)
        embed.add_field(name='Self Assignable Roles On ' + message.server.name, value='```\n' + role_list + '\n```')
    await cmd.bot.send_message(message.channel, None, embed=embed)
