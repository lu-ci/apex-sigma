import arrow
import discord
from sigma.core.permission import check_man_msg, check_admin
from sigma.core.utils import user_avatar


async def textunmute(cmd, message, args):
    if not check_man_msg(message.author, message.channel):
        response = discord.Embed(title='⛔ Unpermitted. Manage Messages Permission Needed.', color=0xDB0000)
    else:
        if not message.mentions:
            response = discord.Embed(title='❗ No user targeted.', color=0xDB0000)
        else:
            target = message.mentions[0]
            if target.id != message.author.id or check_admin(target, message.channel):
                try:
                    mute_list = cmd.db.get_settings(message.guild.id, 'MutedUsers')
                except:
                    mute_list = []
                if target.id not in mute_list:
                    response = discord.Embed(title='❗ User is not muted.', color=0xDB0000)
                else:
                    mute_list.remove(target.id)
                    cmd.db.set_settings(message.guild.id, 'MutedUsers', mute_list)
                    response = discord.Embed(color=0x66CC66,
                                             title=f'✅ {target.name}#{target.discriminator} has been unmuted.')
                    try:
                        log_channel_id = cmd.db.get_settings(message.guild.id, 'LoggingChannel')
                    except:
                        log_channel_id = None
                    if log_channel_id:
                        log_channel = discord.utils.find(lambda x: x.id == log_channel_id, message.guild.channels)
                        if log_channel:
                            log_embed = discord.Embed(color=0x696969, timestamp=arrow.utcnow().datetime)
                            log_embed.set_author(name='A Member Has Been Unmuted', icon_url=user_avatar(target))
                            log_embed.add_field(name='🔊 Unmuted User',
                                                value=f'{target.mention}\n{target.name}#{target.discriminator}',
                                                inline=True)
                            author = message.author
                            log_embed.add_field(name='🛡 Responsible',
                                                value=f'{author.mention}\n{author.name}#{author.discriminator}',
                                                inline=True)
                            if len(args) > 1:
                                log_embed.add_field(name='📄 Reason', value=' '.join(args[1:]), inline=False)
                            log_embed.set_footer(text=f'UserID: {target.id}')
                            await log_channel.send(embed=log_embed)
            else:
                response = discord.Embed(title='❗ You can\'t unmute yourself.', color=0xDB0000)
    await message.channel.send(embed=response)
