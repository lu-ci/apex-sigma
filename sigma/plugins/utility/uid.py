async def uid(cmd, message, args):
    if message.mentions:
        user_q = message.mentions[0]
        out = user_q.nick + '\'s User ID is `' + user_q.id + '`'
    else:
        user_q = message.author
        out = 'Your User ID is `' + user_q.id + '`'
    await cmd.bot.send_message(message.channel, out)
