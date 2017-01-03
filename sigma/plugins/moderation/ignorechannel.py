from sigma.core.permission import check_admin


async def ignorechannel(cmd, message, args):
    if check_admin(message.author, message.channel):
        target = None
        if not args:
            await cmd.bot.send_message(message.channel, cmd.help())
            return
        qry = ' '.join(args)
        if qry.startswith('<#'):
            search_id = qry.replace('<#', '').replace('>', '')
        else:
            search_id = args[0]
        for chan in message.server.channels:
            if chan.id == search_id:
                target = chan
                break
        if not target:
            await cmd.bot.send_message(message.channel, ':notebook: No channel like that was found on this server.')
            return
        else:
            if target == message.author:
                await cmd.bot.send_message(message.channel, 'You can\'t blacklist yourself.')
                return
            if target == cmd.bot.user:
                await cmd.bot.send_message(message.channel, 'You can\'t blacklist me.')
                return
            black = cmd.db.get_settings(message.server.id, 'BlacklistedChannels')
            if not black:
                black = []
            if target.id in black:
                black.remove(target.id)
                await cmd.bot.send_message(message.channel,
                                           ':unlock: The channel **' + target.name + '** has been **un-blacklisted**.')
            else:
                black.append(target.id)
                await cmd.bot.send_message(message.channel,
                                           ':lock: The channel **' + target.name + '** has been **blacklisted**.')
            cmd.db.set_settings(message.server.id, 'BlacklistedChannels', black)
    else:
        await cmd.bot.send_message(message.channel, ':x: Insufficient Permissions.\nServer admin only.')
