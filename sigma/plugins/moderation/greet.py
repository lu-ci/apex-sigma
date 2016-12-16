from sigma.core.permission import check_admin


async def greet(cmd, message, args):
    if not check_admin(message.author, message.channel):
        await cmd.bot.send_message(message.channel, ':x: Insufficient permissions.\nServer admin only.')
        return
    else:
        active = cmd.db.get_settings(message.server.id, 'Greet')
        greet_channel = cmd.db.get_settings(message.server.id, 'GreetChannel')
        if not greet_channel:
            greet_channel = message.server.default_channel.id
        if not active:
            cmd.db.set_settings(message.server.id, 'Greet', True)
            cmd.db.set_settings(message.server.id, 'GreetChannel', message.channel.id)
            await cmd.bot.send_message(message.channel,
                                       ':white_check_mark: Greeting new members has been **enabled** on <#' + message.channel.id + '>.')
        else:
            if message.channel.id == greet_channel:
                cmd.db.set_settings(message.server.id, 'Greet', False)
                await cmd.bot.send_message(message.channel, ':fire: Greeting new members has been **disabled**.')
            else:
                cmd.db.set_settings(message.server.id, 'GreetChannel', message.channel.id)
                await cmd.bot.send_message(message.channel,
                                           ':white_check_mark: The greeting message channel has been changed to <#' + message.channel.id + '>.')
