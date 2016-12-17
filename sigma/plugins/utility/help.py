import asyncio
import discord
from config import Prefix


async def help(cmd, message, args):
    help_msg = None
    timeout = 60
    if not args:
        help_out = discord.Embed(type='rich', title=':grey_question: Help', color=0x1B6F5F)
        help_out.set_author(name='Apex Sigma', url='https://auroraproject.xyz/',
                            icon_url='https://i.imgur.com/s0aVvn7.png')
        help_out.add_field(name='Website', value='[**LINK**](https://auroraproject.xyz/)')
        help_out.add_field(name='Commands', value='[**LINK**](https://auroraproject.xyz/commands)')
        help_out.add_field(name='GitHub', value='[**LINK**](https://github.com/aurora-pro/apex-sigma)')
        help_out.set_footer(
            text='For additional info and help on how to use a command use [' + Prefix + 'help COMMAND].')
        help_msg = await cmd.bot.send_message(message.channel, None, embed=help_out)
    else:
        try:
            help_out = discord.Embed(type='rich', title=':book: ' + args[0].title() + ' Help', color=0x1B6F5F)
            help_out.add_field(name=args[0].title(), value=cmd.bot.plugin_manager.commands[args[0]].help())
            help_msg = await cmd.bot.send_message(message.channel, None, embed=help_out)
        except:
            help_msg = await cmd.bot.send_message(message.channel, ':mag: No such command was found...')
            timeout = 15

    await asyncio.sleep(timeout)

    try:
        await cmd.bot.delete_message(help_msg)
    except:
        pass
    try:
        await cmd.bot.delete_message(message)
    except:
        pass
