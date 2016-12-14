from sigma.core.permission import check_admin


async def unflip(cmd, message, args):
    if check_admin(message.author, message.channel):
        active = cmd.db.get_settings(message.server.id, 'Unflip')
        if active:
            cmd.db.set_settings(message.server.id, 'Unflip', False)
            await cmd.bot.send_message(message.channel, 'Unflip settings toggled to **Disabled**')
        else:
            cmd.db.set_settings(message.server.id, 'Unflip', True)
            await cmd.bot.send_message(message.channel, 'Unflip settings toggled to **Enabled**')
    else:
        await cmd.bot.send_message(message.channel, 'Insufficient permissions.')
