from sigma.core.permission import check_man_roles
from sigma.core.rolecheck import matching_role
import discord


async def clrrole(cmd, message, args):
    if not check_man_roles(message.author, message.channel):
        out_content = discord.Embed(type='rich', color=0xDB0000,
                                    title='⛔ Requires the Manage Roles Permission.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    if not args:
        out_content = discord.Embed(type='rich', color=0xDB0000,
                                    title=':exclamation: Missing Arguments.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    qry = ' '.join(args[1:])
    clr = args[0].replace('#', '')
    try:
        clr_int = int(clr, 16)
        clr_obj = discord.Colour(clr_int)
    except:
        out_content = discord.Embed(type='rich', color=0xDB0000,
                                    title=':exclamation: Invalid Color. Please use HEX.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    role = matching_role(message.server, qry)
    if not role:
        out_content = discord.Embed(type='rich', color=0xFF9900,
                                    title=':warning: ' + qry + ' was not found.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    await cmd.bot.edit_role(message.server, role, color=clr_obj)
    edit_success = discord.Embed(type='rich', color=0x66cc66,
                                 title='✅ Color Changed.')
    await cmd.bot.send_message(message.channel, None, embed=edit_success)
