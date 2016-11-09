import asyncio


async def help(cmd, message, args):
    help_msg = None
    timeout = 60
    if not args:
        help_msg = await cmd.bot.send_message(message.channel, '**Command List**:\n<https://github.com/aurora-pro/apex-sigma/blob/dev/COMMANDLIST.md>')

    else:
        try:
            help_msg = await cmd.bot.send_message(message.channel, cmd.bot.plugin_manager.commands[args[0]].help())
        except:
            help_msg = await cmd.bot.send_message(message.channel, 'No such command...')
            timeout = 15

    await asyncio.sleep(timeout)

    try:
        await cmd.bot.delete_message(help_msg)
        await cmd.bot.delete_message(message)
    except Exception as e:
        cmd.log.error('Help Message Deletion Failed {:s}'.format(e))
