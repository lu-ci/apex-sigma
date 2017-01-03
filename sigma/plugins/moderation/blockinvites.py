from sigma.core.permission import check_admin


async def blockinvites(cmd, message, args):
    if not check_admin(message.author, message.channel):
        await cmd.bot.send_message(message.channel, ':x: Insufficient permissions.\nServer admin only.')
        return
    else:
        active = cmd.db.get_settings(message.server.id, 'BlockInvites')
        if active:
            cmd.db.set_settings(message.server.id, 'BlockInvites', False)
            state = '**Disabled**.'
        else:
            cmd.db.set_settings(message.server.id, 'BlockInvites', True)
            state = '**Enabled**.'
        await cmd.bot.send_message(message.channel, 'Blocking of invites has been ' + state)


