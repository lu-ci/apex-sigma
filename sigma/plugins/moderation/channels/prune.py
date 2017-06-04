import arrow
import discord
import asyncio
from sigma.core.permission import check_man_msg
from sigma.core.utils import user_avatar


async def prune(cmd, message, args):
    channel = message.channel
    if check_man_msg(message.author, channel):
        limit = 100
        target = cmd.bot.user
        if not args:
            limit = 100
            target = cmd.bot.user
        if len(args) == 1 and message.mentions:
            limit = 100
            target = message.mentions[0]
        if len(args) > 1 and message.mentions:
            target = message.mentions[0]
            limit = abs(int(args[0]))
        if len(args) == 1 and not message.mentions:
            target = None
            limit = abs(int(args[0]))
        try:
            await message.delete()
        except:
            pass

        def author_check(msg):
            return msg.author.id == target.id

        if target:
            deleted = await message.channel.purge(limit=limit, check=author_check)
        else:
            deleted = await message.channel.purge(limit=limit)
        embed = discord.Embed(color=0x66CC66, title=f'✅ Deleted {len(deleted)} Messages')
        try:
            log_channel_id = cmd.db.get_settings(message.guild.id, 'LoggingChannel')
        except:
            log_channel_id = None
        if log_channel_id:
            log_channel = discord.utils.find(lambda x: x.id == log_channel_id, message.guild.channels)
            if log_channel:
                response = discord.Embed(color=0x696969, timestamp=arrow.utcnow().datetime)
                response.set_author(name=f'#{channel.name} Has Been Pruned', icon_url=user_avatar(message.author))
                if target:
                    target_text = f'{target.mention}'
                else:
                    target_text = 'No Filter'
                response.add_field(name='🗑 Prune Details',
                                   value=f'Amount: {len(deleted)} Messages\nTarget: {target_text}', inline=True)
                author = message.author
                response.add_field(name='🛡 Responsible',
                                   value=f'{author.mention}\n{author.name}#{author.discriminator}',
                                   inline=True)
                response.set_footer(text=f'ChannelID: {channel.id}')
                await log_channel.send(embed=response)
    else:
        embed = discord.Embed(title='⚠ Unpermitted. Only Those With The Manage Message Permission Allowed.',
                              color=0xDB0000)
    notify_msg = await message.channel.send(None, embed=embed)
    await asyncio.sleep(5)
    try:
        await notify_msg.delete()
    except:
        pass
