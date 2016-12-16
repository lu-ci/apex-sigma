from config import permitted_id


async def blacksrv(cmd, message, args):
    if message.author.id in permitted_id:
        if not args:
            await cmd.bot.send_message(message.channel, cmd.help())
            return
        target = None
        for server in cmd.bot.servers:
            if server.id == args[0]:
                target = server
                break
        if target:
            black = cmd.db.get_settings(target.id, 'IsBlacklisted')
            if black:
                cmd.db.set_settings(target.id, 'IsBlacklisted', False)
                await cmd.bot.send_message(message.channel,
                                           ':unlock: Server **' + target.name + '** has been **un-blacklisted**.')
            else:
                cmd.db.set_settings(target.id, 'IsBlacklisted', True)
                await cmd.bot.send_message(message.channel, ':lock: Server **' + target.name + '** has been **blacklisted**.')
        else:
            await cmd.bot.send_message(message.channel, ':notebook: No server by that ID was found.')
    else:
        await cmd.bot.send_message(message.channel, ':no_entry_sign: Insufficient permissions.')
