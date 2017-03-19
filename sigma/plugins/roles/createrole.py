import discord
from sigma.core.permission import check_man_roles
from sigma.core.rolecheck import matching_role


async def createrole(cmd, message, args):
    if not check_man_roles(message.author, message.channel):
        out_content = discord.Embed(type='rich', color=0xDB0000,
                                    title=':no_entry: Insufficient Permissions. Server Admin Only.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    if not args:
        out_content = discord.Embed(type='rich', color=0xDB0000, title=':exclamation: Error')
        out_content.add_field(name='Not Enough Arguments', value=cmd.help())
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    role_qry = ' '.join(args)
    exists = matching_role(message.server, role_qry)
    if exists:
        out_content = discord.Embed(type='rich', color=0xFF9900, title=':warning: Error')
        out_content.add_field(name='Role Exists', value='A role with the name **' + role_qry + '** already exists.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
    else:
        out_content = discord.Embed(type='rich', color=0x33CC33,
                                    title='✅ Role ' + role_qry + ' created.')
        await cmd.bot.create_role(message.server, name=role_qry)
        await cmd.bot.send_message(message.channel, None, embed=out_content)
