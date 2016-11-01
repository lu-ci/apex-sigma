async def avatar(cmd, message, args):
    if message.mentions:
        target = message.mentions[0]
        ava_url = target.avatar_url
        await cmd.reply(ava_url)
    else:
        await cmd.reply(cmd.help())
