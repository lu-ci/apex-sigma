from .vn_char import key_char_parse


async def keyroute(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    else:
        char_id = args[0].replace('c', '')
        res = key_char_parse(char_id)
        print(res)
