from sigma.core.permission import check_man_roles
from sigma.core.rolecheck import matching_role
import discord


async def delselfrole(cmd, message, args):
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
    target_role = matching_role(message.server, role_qry)
    if not target_role:
        out_content = discord.Embed(type='rich', color=0xFF9900, title=':exclamation: Error')
        out_content.add_field(name='Role Not Found', value='I was unable to find **' + role_qry + '** on this server.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
    else:
        try:
            self_roles = cmd.db.get_settings(message.server.id, 'SelfRoles')
        except:
            cmd.db.set_settings(message.server.id, 'SelfRoles', [])
            self_roles = []
        if target_role.name in self_roles:
            self_roles.remove(target_role.name)
            cmd.db.set_settings(message.server.id, 'SelfRoles', self_roles)
            out_content = discord.Embed(type='rich', color=0x66cc66,
                                        title=':white_check_mark: Role **' + target_role.name + '** removed from the self assignable roles list.')
            await cmd.bot.send_message(message.channel, None, embed=out_content)
        else:
            out_content = discord.Embed(type='rich', color=0xFF9900, title=':warning: Error')
            out_content.add_field(name='Role Not Self Assignable',
                                  value='I was unable to find **' + role_qry + '** in the list of self assignable roles.')
            await cmd.bot.send_message(message.channel, None, embed=out_content)
