import discord
from config import Prefix


async def help(cmd, message, args):
    if not args:
        help_out = discord.Embed(type='rich', title=':grey_question: Help', color=0x1B6F5F)
        help_out.set_author(name='Apex Sigma', url='https://auroraproject.xyz/',
                            icon_url='https://i.imgur.com/s0aVvn7.png')
        help_out.add_field(name='Website', value='[**LINK**](https://auroraproject.xyz/)')
        help_out.add_field(name='Commands', value='[**LINK**](https://auroraproject.xyz/commands)')
        help_out.add_field(name='GitHub', value='[**LINK**](https://github.com/aurora-pro/apex-sigma)')
        help_out.set_footer(
            text='For additional info and help on how to use a command use [' + Prefix + 'help COMMAND].')
        await cmd.bot.send_message(message.channel, None, embed=help_out)
    else:
        try:
            help_out = discord.Embed(type='rich', title=':book: ' + args[0].title() + ' Help', color=0x1B6F5F)
            help_out.add_field(name=args[0].title(), value=cmd.bot.plugin_manager.commands[args[0]].help())
            await cmd.bot.send_message(message.channel, None, embed=help_out)
        except:
            out_content = discord.Embed(type='rich', color=0xDB0000,
                                        title=':mag: No such command was found...')
            await cmd.bot.send_message(message.channel, None, embed=out_content)
