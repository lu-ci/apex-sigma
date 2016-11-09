async def sid(cmd, message, args):
    if message.server:
        await cmd.bot.send_message(message.channel, 'The Server ID of **' + message.server.name + '** is `' + message.server.id + '`')
    else:
        await cmd.bot.send_message(message.channel, 'This is unusable in Direct Messsages as direct messages have no message channel.')
