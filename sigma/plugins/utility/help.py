import asyncio
from config import Prefix

async def help(cmd, message, args):
    help_msg = None
    timeout = 60
    if not args:
        help_out = '**Website:**\n<https://auroraproject.xyz/>'
        help_out += '\n**Command List**:\n<https://auroraproject.xyz/commands>'
        help_out += '\n**Command List (GitHub)**:\n<https://github.com/aurora-pro/apex-sigma/blob/dev/COMMANDLIST.md>'
        help_out += '\n\nTo get help with a certain command, you can type `' + Prefix + 'help COMMAND`'
        help_msg = await cmd.bot.send_message(message.channel, help_out)

    else:
        try:
            help_msg = await cmd.bot.send_message(message.channel, cmd.bot.plugin_manager.commands[args[0]].help())
        except:
            help_msg = await cmd.bot.send_message(message.channel, 'No such command...')
            timeout = 15

    await asyncio.sleep(timeout)

    try:
        await cmd.bot.delete_message(help_msg)
    except Exception as e:
        cmd.log.error('Help Message Deletion Failed {:s}'.format(e))
    try:
        await cmd.bot.delete_message(message)
    except Exception as e:
        cmd.log.error('Help Message Deletion Failed {:s}'.format(e))
