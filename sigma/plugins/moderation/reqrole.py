import discord
from sigma.core.permission import check_admin
from sigma.core.rolecheck import matching_role


async def reqrole(cmd, message, args):
    if not check_admin(message.author, message.channel):
        out_content = discord.Embed(type='rich', color=0xDB0000,
                                    title=':no_entry: Insufficient Permissions. Server Admin Only.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    try:
        current_role = cmd.db.get_settings(message.server.id, 'RequiredRole')
    except KeyError:
        cmd.db.set_settings(message.server.id, 'RequiredRole', None)
        current_role = None
    if not args:
        if current_role:
            embed = discord.Embed(title=':information_source: Current Required Role Is ' + current_role, color=0x0099FF)
        else:
            embed = discord.Embed(title=':warning: Currently There Is No Role Requirement For Using Sigma',
                                  color=0xFF9900)
        await cmd.bot.send_message(message.channel, None, embed=embed)
    else:
        mat_role = matching_role(message.server, ' '.join(args))
        if not mat_role:
            embed = discord.Embed(title=':exclamation: That role was not found on the server.',
                                  color=0xDB0000)
        else:
            cmd.db.set_settings(message.server.id, 'RequiredRole', str(mat_role.name))
            embed = discord.Embed(title=':white_check_mark: ' + mat_role.name + ' Set As The Required Role',
                                  color=0x33CC33)
        await cmd.bot.send_message(message.channel, None, embed=embed)
