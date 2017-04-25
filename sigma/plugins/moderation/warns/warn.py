import discord
import arrow
from sigma.core.permission import check_kick


async def warn(cmd, message, args):
    if not check_kick(message.author, message.channel):
        out_content = discord.Embed(color=0xDB0000,
                                    title='⛔ Users With Kick Permissions Only.')
        await message.channel.send(None, embed=out_content)
        return
    if not args or not message.mentions:
        return
    target = message.mentions[0]
    warning_text = ' '.join(args).replace(target.mention, '')[1:]
    if not warning_text or warning_text == '':
        warning_text = 'No Reason Given'
    try:
        warn_limit = cmd.db.get_settings(message.guild.id, 'WarnLimit')
    except KeyError:
        cmd.db.set_settings(message.guild.id, 'WarnLimit', 2)
        warn_limit = 2
    try:
        warned_users = cmd.db.get_settings(message.guild.id, 'WarnedUsers')
    except KeyError:
        cmd.db.set_settings(message.guild.id, 'WarnedUsers', {})
        warned_users = {}
    target_id = str(target.id)
    if target_id in warned_users:
        warn_data = {
            'UserID': warned_users[target_id]['UserID'],
            'Warns': warned_users[target_id]['Warns'] + 1,
            'Reasons': warned_users[target_id]['Reasons'] + [warning_text],
            'Timestamp': arrow.utcnow().timestamp
        }
    else:
        warn_data = {
            'UserID': target.id,
            'Warns': 1,
            'Reasons': [warning_text],
            'Timestamp': arrow.utcnow().timestamp
        }
    warned_users.update({target_id: warn_data})
    if warned_users[target_id]['Warns'] > warn_limit:
        await cmd.bot.kick(target)
        out_content_local = discord.Embed(color=0x993300)
        out_content_local.add_field(name=':boot: User **' + target.name + '** has been kicked!',
                                    value='Reasons:\n```\n' + '\n'.join(warned_users[target_id]['Reasons']) + '\n```')
        await message.channel.send(None, embed=out_content_local)
        out_content_to_user = discord.Embed(color=0x993300)
        out_content_to_user.add_field(name=':boot: You have been kicked!',
                                      value='Reasons:\n```\n' + '\n'.join(warned_users[target_id]['Reasons']) + '\n```')
        await target.send(None, embed=out_content_to_user)
        del warned_users[target_id]
    else:
        warned_users.update({target_id: warn_data})
        out_content_to_user = discord.Embed(color=0xFF9900)
        out_content_to_user.add_field(name='⚠ Warning ' + str(warned_users[target_id]['Warns']) + '/' + str(
            warn_limit) + ' on ' + message.guild.name, value='Reason:\n```\n' + warning_text + '\n```')
        await target.send(None, embed=out_content_to_user)
        out_content_local = discord.Embed(color=0xFF9900, title='⚠ Warning ' + str(
            warned_users[target_id]['Warns']) + '/' + str(
            warn_limit) + ' for ' + target.name)
        await message.channel.send(None, embed=out_content_local)
    cmd.db.set_settings(message.guild.id, 'WarnedUsers', warned_users)
