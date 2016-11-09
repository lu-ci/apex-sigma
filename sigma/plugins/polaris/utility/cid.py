async def cid(cmd, message, args):
    if message.server:
        chn_id = message.channel.id
        if args:
            arguments = ' '.join(args)
            if arguments.startswith('<#'):
                chn_id = arguments[2:-1]
        await cmd.bot.send_message(message.channel, 'The Channel ID of <#' + chn_id + '> is `' + chn_id + '`')
    else:
        await cmd.bot.send_message(message.channel, 'This is unusable in Direct Messsages as direct messages have no host server.')
