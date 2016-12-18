from sigma.core.permission import check_admin


async def autorole(cmd, message, args):
    if not check_admin(message.author, message.channel):
        out_content = cmd.embed(type='rich', color=0xDD0000)
        await cmd.bot.send_message(message.channel, None, embed=out_content)
