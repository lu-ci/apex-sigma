from sigma.core.permission import check_admin


async def greetmsg(cmd, message, args):
    if message.server:
        if not args:
            greet_message = cmd.db.get_settings(message.server.id, 'GreetMessage')
            await cmd.bot.send_message(message.channel,
                                       'The current greet message is:\n```\n' + greet_message + '\n```')
        else:
            if not check_admin(message.author, message.channel):
                await cmd.bot.send_message(message.channel, ':x: Insufficient permissions.\nServer admin only.')
                return
            else:
                new_message = ' '.join(args)
                cmd.db.set_settings(message.server.id, 'GreetMessage', new_message)
                await cmd.bot.send_message(message.channel, 'The new greet message has been set.')
