import discord


async def permissions(cmd, message, args):
    allowed_list = []
    disallowed_list = []
    if args:
        user_q = message.mentions[0]
    else:
        user_q = message.author
    embed = discord.Embed(title='ℹ ' + user_q.name + '\'s Permissions', color=0x0099FF)
    for permission in user_q.guild_permissions:
        if permission[1]:
            allowed_list.append(permission[0].replace('_', ' ').title())
        else:
            disallowed_list.append(permission[0].replace('_', ' ').title())
    if len(allowed_list) == 0:
        allowed_list = ['None']
    if len(disallowed_list) == 0:
        disallowed_list = ['None']
    embed.add_field(name='Allowed', value='```\n - ' + '\n - '.join(sorted(allowed_list)) + '\n```')
    embed.add_field(name='Disallowed', value='```\n - ' + '\n - '.join(sorted(disallowed_list)) + '\n```')
    await message.channel.send(None, embed=embed)
