import discord
from sigma.core.permission import check_kick


async def warns(cmd, message, args):
    if not check_kick(message.author, message.channel):
        out_content = discord.Embed(color=0xDB0000,
                                    title=':no_entry: Users With Kick Permissions Only.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    try:
        warned_users = cmd.db.get_settings(message.server.id, 'WarnedUsers')
    except KeyError:
        cmd.db.set_settings(message.server.id, 'WarnedUsers', {})
        warned_users = {}
    if not message.mentions:
        if len(warned_users) == 0:
            embed = discord.Embed(color=0x0099FF, title='ℹ There Are No Warned Users')
        else:
            warn_user_list = []
            for key in warned_users:
                for member in message.server.members:
                    if member.id == warned_users[key]['UserID']:
                        warn_user_list.append(member.name)
            embed = discord.Embed(color=0x0099FF)
            embed.add_field(name='ℹ List of Warned Users', value='```\n' + ', '.join(warn_user_list) + '\n```')
    else:
        target = message.mentions[0]
        if target.id not in warned_users:
            embed = discord.Embed(color=0x0099FF, title='ℹ ' + target.name + ' Was Never Warned')
        else:
            embed = discord.Embed(color=0x0099FF)
            embed.add_field(name='ℹ ' + target.name + ' Was Warned For...',
                            value='```\n' + '\n'.join(warned_users[target.id]['Reasons']) + '\n```')
    await cmd.bot.send_message(message.channel, None, embed=embed)
