async def avatar(cmd, message, args):
    if message.mentions:
        target = message.mentions[0]
        ava_url = target.avatar_url
        await cmd.bot.send_message(message.channel, ava_url)
    else:
        await cmd.bot.send_message(message.channel, cmd.help())
