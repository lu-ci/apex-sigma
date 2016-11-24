async def keyroute(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    else:
        if len(args) < 2:
            await cmd.bot.send_message(message.channel, cmd.help())
            return
        else:
            visual_novel = ' '.join(args[:-1])
            character = args[-1]

