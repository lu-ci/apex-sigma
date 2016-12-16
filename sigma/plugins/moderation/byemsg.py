from sigma.core.permission import check_admin


async def byemsg(cmd, message, args):
    if message.server:
        if not args:
            greet_message = cmd.db.get_settings(message.server.id, 'ByeMessage')
            await cmd.bot.send_message(message.channel,
                                       'The current bye message is:\n```\n' + greet_message + '\n```')
        else:
            if not check_admin(message.author, message.channel):
                await cmd.bot.send_message(message.channel, ':x: Insufficient permissions.\nServer admin only.')
                return
            else:
                new_message = ' '.join(args)
                cmd.db.set_settings(message.server.id, 'ByeMessage', new_message)
                await cmd.bot.send_message(message.channel, 'The new bye message has been set.')
