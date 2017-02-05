import discord
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

        def author_check(msg):
            return msg.author == target
        if target:
            deleted = await cmd.bot.purge_from(message.channel, limit=limit, check=author_check)
        else:
            deleted = await cmd.bot.purge_from(message.channel, limit=limit)
        embed = discord.Embed(color=0x66CC66, title=':white_check_mark: Deleted ' + str(len(deleted)) + ' Messages')
    else:
        embed = discord.Embed(title=':warning: Unpermitted. Only Those With The Manage Message Permission Allowed.',
                              color=0xDB0000)
    await cmd.bot.send_message(message.channel, None, embed=embed)
