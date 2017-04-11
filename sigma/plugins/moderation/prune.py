import discord
import asyncio
from sigma.core.permission import check_man_msg


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
    else:
        embed = discord.Embed(title='⚠ Unpermitted. Only Those With The Manage Message Permission Allowed.',
                              color=0xDB0000)
    notify_msg = await message.channel.send(None, embed=embed)
    await asyncio.sleep(5)
    try:
        await notify_msg.delete()
    except:
        pass
