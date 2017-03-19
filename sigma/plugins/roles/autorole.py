from sigma.core.permission import check_admin
from sigma.core.rolecheck import matching_role
import discord


async def autorole(cmd, message, args):
    if not check_admin(message.author, message.channel):
        out_content = discord.Embed(type='rich', color=0xDB0000,
                                    title='⛔ Insufficient Permissions. Server Admin Only.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    try:
        current_role = cmd.db.get_settings(message.server.id, 'AutoRole')
    except KeyError:
        cmd.db.set_settings(message.server.id, 'AutoRole', None)
        current_role = None
    if not args:
        if current_role:
            out_content = discord.Embed(type='rich', color=0x0099FF,
                                        title=':information_source: Current Auto Role: ' + current_role)
            await cmd.bot.send_message(message.channel, None, embed=out_content)
            return
        else:
            out_content = discord.Embed(type='rich', color=0x0099FF,
                                        title=':information_source: No Auto Role Set')
            await cmd.bot.send_message(message.channel, None, embed=out_content)
            return
    role_qry = ' '.join(args)
    role_qry_low = role_qry.lower()
    if role_qry_low == 'disable':
        cmd.db.set_settings(message.server.id, 'AutoRole', None)
        out_content = discord.Embed(type='rich', color=0x66CC66,
                                    title='✅ Auto Role Disabled and Cleaned.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    target_role = matching_role(message.server, role_qry)
    if current_role and current_role.lower() == role_qry_low:
        out_content = discord.Embed(type='rich', color=0xFF9900, title=':warning: Error')
        out_content.add_field(name='Present Role', value='This Role is already the Auto Role for this server.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    if target_role:
        cmd.db.set_settings(message.server.id, 'AutoRole', role_qry)
        out_content = discord.Embed(type='rich', color=0x33CC33)
        out_content.add_field(name='✅ Success',
                              value='The role **' + role_qry + '** has been set as the Auto Role.')
    else:
        out_content = discord.Embed(type='rich', color=0xDB0000, title=':exclamation: Error')
        out_content.add_field(name='Role Not Found', value='I have not found **' + role_qry + '** on this server.')
    await cmd.bot.send_message(message.channel, None, embed=out_content)
