async def sid(cmd, message, args):
    if message.server:
        await cmd.reply('The Server ID of **' + message.server.name + '** is `' + message.server.id + '`')
    else:
        await cmd.reply('This is unusable in Direct Messsages as direct messages have no message channel.')
