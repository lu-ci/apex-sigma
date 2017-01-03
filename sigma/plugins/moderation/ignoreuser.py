from sigma.core.permission import check_admin


async def ignoreuser(cmd, message, args):
    if check_admin(message.author, message.channel):
        target = None
        if not args:
            await cmd.bot.send_message(message.channel, cmd.help())
            return
        if message.mentions:
            target = message.mentions[0]
        else:
            for user in message.server.members:
                if user.id == args[0]:
                    target = user
                    break
        if not target:
            await cmd.bot.send_message(message.channel, ':notebook: No user like that was found on this server.')
            return
        else:
            if target == message.author:
                await cmd.bot.send_message(message.channel, 'You can\'t blacklist yourself.')
                return
            if target == cmd.bot.user:
                await cmd.bot.send_message(message.channel, 'You can\'t blacklist me.')
                return
            black = cmd.db.get_settings(message.server.id, 'BlacklistedUsers')
            if not black:
                black = []
            if target.id in black:
                black.remove(target.id)
                await cmd.bot.send_message(message.channel,
                                           ':unlock: The user **' + target.name + '** has been **un-blacklisted**.')
            else:
                black.append(target.id)
                await cmd.bot.send_message(message.channel,
                                           ':lock: The user **' + target.name + '** has been **blacklisted**.')
            cmd.db.set_settings(message.server.id, 'BlacklistedUsers', black)
    else:
        await cmd.bot.send_message(message.channel, ':x: Insufficient Permissions.\nServer admin only.')
