import asyncio


async def help(cmd, message, args):
    help_msg = None

    if not args:
        help_msg = await cmd.reply(cmd.help())

    else:
        help_msg = await cmd.reply(cmd.bot.plugin_manager.commands[args[0]].help())

    await asyncio.sleep(60)

    try:
        await cmd.bot.delete_message(help_msg)
    except Exception as e:
        cmd.log.error('Help Message Deletion Failed {:s}'.format(e))
