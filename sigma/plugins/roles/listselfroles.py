import discord


async def listselfroles(cmd, message, args):
    self_roles = cmd.db.get_settings(message.guild.id, 'SelfRoles')
    role_list = []
    for srv_role in message.guild.roles:
        for role in self_roles:
            if role == srv_role.id:
                role_list.append(srv_role.name)
    if role_list == '':
        embed = discord.Embed(type='rich', color=0x0099FF,
                              title='ℹ No Self Assignable Roles Set')
    else:
        rl_out = ''
        role_list = sorted(role_list)
        for rl in role_list:
            rl_out += '\n - ' + rl
        embed = discord.Embed(color=0x1ABC9C)
        embed.add_field(name='Self Assignable Roles On ' + message.guild.name, value='```\n' + rl_out + '\n```')
    await message.channel.send(None, embed=embed)
