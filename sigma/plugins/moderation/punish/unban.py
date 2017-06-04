from sigma.core.permission import check_ban
from sigma.core.utils import user_avatar
import discord
import arrow


async def unban(cmd, message, args):
    if not check_ban(message.author, message.channel):
        response = discord.Embed(title='⛔ Unpermitted. Ban Permissions Needed.', color=0xDB0000)
    else:
        if args:
            user_search = ' '.join(args)
            target = None
            banlist = await message.guild.bans()
            for entry in banlist:
                if entry.user.name.lower() == user_search.lower():
                    target = entry.user
                    break
            if target:
                await message.guild.unban(target,
                                          reason=f'Unbanned by {message.author.name}#{message.author.discriminator}.')
                response = discord.Embed(title=f'✅ {target.name} has been unbanned.', color=0x66CC66)
                # Logging Part
                try:
                    log_channel_id = cmd.db.get_settings(message.guild.id, 'LoggingChannel')
                except:
                    log_channel_id = None
                if log_channel_id:
                    log_channel = discord.utils.find(lambda x: x.id == log_channel_id, message.guild.channels)
                    if log_channel:
                        log_response = discord.Embed(color=0x993300, timestamp=arrow.utcnow().datetime)
                        log_response.set_author(name=f'A User Has Been Unbanned', icon_url=user_avatar(target))
                        log_response.add_field(name='🔨 Unbanned User',
                                               value=f'{target.mention}\n{target.name}#{target.discriminator}',
                                               inline=True)
                        author = message.author
                        log_response.add_field(name='🛡 Responsible',
                                               value=f'{author.mention}\n{author.name}#{author.discriminator}',
                                               inline=True)
                        log_response.set_footer(text=f'UserID: {target.id}')
                        await log_channel.send(embed=log_response)
            else:
                response = discord.Embed(title=f'🔍 {user_search} not found in the ban list.')
        else:
            response = discord.Embed(title='❗ No user targeted.', color=0xDB0000)
    await message.channel.send(embed=response)
