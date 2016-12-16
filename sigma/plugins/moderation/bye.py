from sigma.core.permission import check_admin


async def bye(cmd, message, args):
    if not check_admin(message.author, message.channel):
        await cmd.bot.send_message(message.channel, ':x: Insufficient permissions.\nServer admin only.')
        return
    else:
        active = cmd.db.get_settings(message.server.id, 'Bye')
        bye_channel = cmd.db.get_settings(message.server.id, 'ByeChannel')
        if not bye_channel:
            bye_channel = message.server.default_channel.id
        if not active:
            cmd.db.set_settings(message.server.id, 'Bye', True)
            cmd.db.set_settings(message.server.id, 'ByeChannel', message.channel.id)
            await cmd.bot.send_message(message.channel,
                                       ':white_check_mark: Notifying of leaving members has been **enabled** on <#' + message.channel.id + '>.')
        else:
            if message.channel.id == bye_channel:
                cmd.db.set_settings(message.server.id, 'Bye', False)
                await cmd.bot.send_message(message.channel,
                                           ':fire: Notifying of leaving members has been **disabled**.')
            else:
                cmd.db.set_settings(message.server.id, 'ByeChannel', message.channel.id)
                await cmd.bot.send_message(message.channel,
                                           ':white_check_mark: The leaving members message channel has been changed to <#' + message.channel.id + '>.')
