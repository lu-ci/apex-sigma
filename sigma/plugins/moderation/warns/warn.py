import discord
import arrow
from sigma.core.permission import check_man_msg
from sigma.core.utils import user_avatar


async def warn(cmd, message, args):
    if not check_man_msg(message.author, message.channel):
        out_content = discord.Embed(color=0xDB0000,
                                    title='⛔ Users With Manage Messages Permissions Only.')
        await message.channel.send(None, embed=out_content)
        return
    if not args or not message.mentions:
        return
    target = message.mentions[0]
    warning_text = ' '.join(args).replace(target.mention, '')[1:]
    if not warning_text or warning_text == '':
        warning_text = 'No Reason Given'
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
    out_content_to_user = discord.Embed(color=0xFF9900)
    out_content_to_user.add_field(name=f'⚠ Warning on {message.guild.name}', value=f'Reason:\n```\n{warning_text}\n```')
    try:
        await target.send(None, embed=out_content_to_user)
    except:
        pass
    out_content_local = discord.Embed(color=0xFF9900, title=f'⚠ {target.name} has been warned.')
    await message.channel.send(None, embed=out_content_local)
    cmd.db.set_settings(message.guild.id, 'WarnedUsers', warned_users)
    # Logging Part
    try:
        log_channel_id = cmd.db.get_settings(message.guild.id, 'LoggingChannel')
    except:
        log_channel_id = None
    if log_channel_id:
        log_channel = discord.utils.find(lambda x: x.id == log_channel_id, message.guild.channels)
        if log_channel:
            response = discord.Embed(color=0xFF9900, timestamp=arrow.utcnow().datetime)
            response.set_author(name=f'A User Has Been Warned', icon_url=user_avatar(target))
            response.add_field(name='⚠ Warned User',
                               value=f'{target.mention}\n{target.name}#{target.discriminator}', inline=True)
            author = message.author
            response.add_field(name='🛡 Responsible',
                               value=f'{author.mention}\n{author.name}#{author.discriminator}',
                               inline=True)
            if warning_text:
                response.add_field(name='📄 Reason', value=f"```\n{warning_text}\n```", inline=False)
            response.set_footer(text=f'UserID: {target.id}')
            await log_channel.send(embed=response)
