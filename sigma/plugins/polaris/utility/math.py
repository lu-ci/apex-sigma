async def math(cmd, message, args):
    if args:
        problem = ''.join(args)
        out_text = eval(problem)
        await cmd.reply(out_text)
    else:
        await cmd.reply(cmd.help())
        return
