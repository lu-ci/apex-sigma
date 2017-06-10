import discord
from sigma.core.permission import check_man_msg


async def warns(cmd, message, args):
    try:
        warned_users = cmd.db.get_settings(message.guild.id, 'WarnedUsers')
    except KeyError:
        cmd.db.set_settings(message.guild.id, 'WarnedUsers', {})
        warned_users = {}
    if not check_man_msg(message.author, message.channel):
        target = message.author
        target_id = str(target.id)
        if target_id not in warned_users:
            embed = discord.Embed(color=0x0099FF, title='ℹ You Were Never Warned')
        else:
            embed = discord.Embed(color=0x0099FF)
            embed.add_field(name='ℹ You Were Warned For...',
                            value='```\n- ' + '\n- '.join(warned_users[target_id]['Reasons']) + '\n```')
        await message.channel.send(None, embed=embed)
        return
    if not message.mentions:
        if len(warned_users) == 0:
            embed = discord.Embed(color=0x0099FF, title='ℹ There Are No Warned Users')
        else:
            warn_user_list = []
            for key in warned_users:
                for member in message.guild.members:
                    if member.id == warned_users[key]['UserID']:
                        warn_user_list.append(f'{member.name}#{member.discriminator}')
            embed = discord.Embed(color=0x0099FF)
            embed.add_field(name='ℹ List of Warned Users', value='```\n' + ', '.join(warn_user_list) + '\n```')
    else:
        target = message.mentions[0]
        target_id = str(target.id)
        if target_id not in warned_users:
            embed = discord.Embed(color=0x0099FF, title='ℹ ' + target.name + ' Was Never Warned')
        else:
            embed = discord.Embed(color=0x0099FF)
            embed.add_field(name='ℹ ' + target.name + ' Was Warned For...',
                            value='```\n- ' + '\n- '.join(warned_users[target_id]['Reasons']) + '\n```')
    await message.channel.send(None, embed=embed)
