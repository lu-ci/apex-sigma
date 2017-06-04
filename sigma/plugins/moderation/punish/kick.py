from sigma.core.permission import check_kick
from sigma.core.utils import user_avatar
import discord
import arrow


async def kick(cmd, message, args):
    if not check_kick(message.author, message.channel):
        response = discord.Embed(title='⛔ Unpermitted. Kick Permissions Needed.', color=0xDB0000)
    else:
        if message.mentions:
            target = message.mentions[0]
            if target.id == message.author.id:
                response = discord.Embed(title='⛔ You can\'t kick yourself.', color=0xDB0000)
            else:
                if len(args) > 1:
                    kick_reason = ' '.join(args[1:])
                else:
                    kick_reason = 'No reason given'
                await target.kick(
                    reason=f'Kicked by {message.author.name}#{message.author.discriminator}.\n{kick_reason}')
                response = discord.Embed(title=f'👢 {target.name} has been kicked.', color=0x993300)
                # Logging Part
                try:
                    log_channel_id = cmd.db.get_settings(message.guild.id, 'LoggingChannel')
                except:
                    log_channel_id = None
                if log_channel_id:
                    log_channel = discord.utils.find(lambda x: x.id == log_channel_id, message.guild.channels)
                    if log_channel:
                        log_response = discord.Embed(color=0x993300, timestamp=arrow.utcnow().datetime)
                        log_response.set_author(name=f'A User Has Been Kicked', icon_url=user_avatar(target))
                        log_response.add_field(name='👢 Kicked User',
                                               value=f'{target.mention}\n{target.name}#{target.discriminator}',
                                               inline=True)
                        author = message.author
                        log_response.add_field(name='🛡 Responsible',
                                               value=f'{author.mention}\n{author.name}#{author.discriminator}',
                                               inline=True)
                        log_response.add_field(name='📄 Reason', value=f"```\n{kick_reason}\n```", inline=False)
                        log_response.set_footer(text=f'UserID: {target.id}')
                        await log_channel.send(embed=log_response)
        else:
            response = discord.Embed(title='❗ No user targeted.', color=0xDB0000)
    await message.channel.send(embed=response)
