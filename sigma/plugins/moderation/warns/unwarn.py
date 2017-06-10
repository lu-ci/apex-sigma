import arrow
import discord
from sigma.core.permission import check_man_msg
from sigma.core.utils import user_avatar


async def unwarn(cmd, message, args):
    if not check_man_msg(message.author, message.channel):
        out_content = discord.Embed(color=0xDB0000,
                                    title='⛔ Users With Manage Messages Permissions Only.')
        await message.channel.send(None, embed=out_content)
        return
    if not args or not message.mentions:
        return
    target = message.mentions[0]
    target_id = str(target.id)
    try:
        warned_users = cmd.db.get_settings(message.guild.id, 'WarnedUsers')
    except KeyError:
        cmd.db.set_settings(message.guild.id, 'WarnedUsers', {})
        warned_users = {}
    if target_id in warned_users:
        del warned_users[target_id]
        cmd.db.set_settings(message.guild.id, 'WarnedUsers', warned_users)
        response = discord.Embed(color=0x66CC66, title=f'✅ {target.name} has been removed from the warning list.')
    else:
        response = discord.Embed(color=0x0099FF, title=f'ℹ {target.name} is not in the list of warned users.')
    await message.channel.send(None, embed=response)
    # Logging Part
    try:
        log_channel_id = cmd.db.get_settings(message.guild.id, 'LoggingChannel')
    except:
        log_channel_id = None
    if log_channel_id:
        log_channel = discord.utils.find(lambda x: x.id == log_channel_id, message.guild.channels)
        if log_channel:
            response = discord.Embed(color=0xFF9900, timestamp=arrow.utcnow().datetime)
            response.set_author(name=f'A User\'s Warnings Have Been Removed', icon_url=user_avatar(target))
            response.add_field(name='⚠ Unwarned User',
                               value=f'{target.mention}\n{target.name}#{target.discriminator}', inline=True)
            author = message.author
            response.add_field(name='🛡 Responsible',
                               value=f'{author.mention}\n{author.name}#{author.discriminator}',
                               inline=True)
            response.set_footer(text=f'UserID: {target.id}')
            await log_channel.send(embed=response)
