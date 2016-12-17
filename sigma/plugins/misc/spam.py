async def spam(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    if len(args) < 2:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    try:
        count = int(args[0])
    except:
        await cmd.bot.send_message(message.channel, 'Invalid input.')
        return
    if count > 20:
        count = 20
    msg = ' '.join(args[1:])
    out = ''
    n = 0
    while n <= count:
        n += 1
        out += msg + ' '
    await cmd.bot.send_message(message.channel, out[:1950])
