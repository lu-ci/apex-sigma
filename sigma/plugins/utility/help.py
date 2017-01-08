import discord
from config import Prefix, MainServerURL


async def help(cmd, message, args):
    if not args:
        help_out = discord.Embed(type='rich', title=':grey_question: Help', color=0x1B6F5F)
        help_out.set_author(name='Apex Sigma', url=MainServerURL,
                            icon_url='https://i.imgur.com/s0aVvn7.png')
        help_out.add_field(name='Website', value='[**LINK**](' + MainServerURL + ')')
        help_out.add_field(name='Commands', value='[**LINK**](' + MainServerURL + 'commands)')
        help_out.add_field(name='GitHub', value='[**LINK**](https://github.com/aurora-pro/apex-sigma)')
        help_out.add_field(name='AP Discord', value='[**LINK**](https://discordapp.com/invite/Ze9EfTd)')
        help_out.add_field(name='Add Me To Discord',
                           value='[**LINK**](https://discordapp.com/oauth2/authorize?client_id=' + cmd.bot.user.id + '&scope=bot&permissions=8)')
        if message.server:
            help_out.add_field(name='Ranking For This Server',
                               value='[**LINK**](' + MainServerURL + 'ranking?sid=' + message.server.id + ')')
        help_out.set_footer(
            text='For additional info and help on how to use a command use [' + Prefix + 'help COMMAND_NAME] (Example: ' + Prefix + 'help slots).')
        await cmd.bot.send_message(message.channel, None, embed=help_out)
    else:
        try:
            help_out = discord.Embed(type='rich', title=':book: ' + args[0].title() + ' Help', color=0x1B6F5F)
            help_out.add_field(name=args[0].title(), value=cmd.bot.plugin_manager.commands[args[0].lower()].help())
            await cmd.bot.send_message(message.channel, None, embed=help_out)
        except:
            out_content = discord.Embed(type='rich', color=0x696969,
                                        title=':mag: No such command was found...')
            await cmd.bot.send_message(message.channel, None, embed=out_content)
