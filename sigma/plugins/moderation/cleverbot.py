from sigma.core.permission import check_admin


async def cleverbot(cmd, message, args):
    if not check_admin(message.author, message.channel):
        await cmd.bot.send_message(message.channel, ':x: Insufficient permissions.\nServer admin only.')
        return
    else:
        active = cmd.db.get_settings(message.server.id, 'CleverBot')
        if active:
            cmd.db.set_settings(message.server.id, 'CleverBot', False)
            state = '**Disabled**.'
        else:
            cmd.db.set_settings(message.server.id, 'CleverBot', True)
            state = '**Enabled**.'
        await cmd.bot.send_message(message.channel, 'The CleverBot functionality has been ' + state)
