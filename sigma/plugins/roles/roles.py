import discord


async def roles(cmd, message, args):
    n = 0
    role_list = ''
    for role in message.server.roles:
        n += 1
        role_list += role.name + ', '
    role_list = role_list[:-2].replace('@', '')
    if len(role_list) > 1800:
        role_list = role_list[:1800] + '...'
    embed = discord.Embed(color=0x1ABC9C)
    embed.add_field(name='There Are ' + str(n) + ' roles on ' + message.server.name,
                    value='```\n' + role_list + '\n```')
    await message.channel.send(None, embed=embed)
