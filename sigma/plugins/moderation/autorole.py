from sigma.core.permission import check_admin
import discord


async def autorole(cmd, message, args):
    if not check_admin(message.author, message.channel):
        out_content = discord.Embed(type='rich', color=0xDB0000, title=':x: Insufficient Permissions. Server Admin Only.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    if not args:
        out_content = discord.Embed(type='rich', color=0xDB0000, title=':exclamation: Error')
        out_content.add_field(name='Not Enough Arguments', value=cmd.help())
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    role_qry = ' '.join(args)
    role_qry_low = role_qry.lower()
    target_role = None
    current_role = cmd.db.get_settings(message.server.id, 'AutoRole')
    if current_role.lower() == role_qry_low:
        out_content = discord.Embed(type='rich', color=0xFF9900, title=':warning: Error')
        out_content.add_field(name='Present Role', value='This Role is already the Auto Role for this server.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    for role in message.server.roles:
        if role.name.lower() == role_qry_low:
            target_role = role
            break
    if target_role:
        cmd.db.set_settings(message.server.id, 'AutoRole', role_qry)
        out_content = discord.Embed(type='rich', color=0x33CC33)
        out_content.add_field(name=':white_check_mark: Success',
                              value='The role **' + role_qry + '** has been set as the Auto Role.')
    else:
        out_content = discord.Embed(type='rich', color=0xDB0000, title=':exclamation: Error')
        out_content.add_field(name='Role Not Found', value='I have not found **' + role_qry + '** on this server.')
    await cmd.bot.send_message(message.channel, None, embed=out_content)
