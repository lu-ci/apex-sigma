from sigma.core.permission import check_admin
from sigma.core.rolecheck import matching_role
import discord


async def autorole(cmd, message, args):
    if not check_admin(message.author, message.channel):
        out_content = discord.Embed(type='rich', color=0xDB0000,
                                    title='⛔ Insufficient Permissions. Server Admin Only.')
        await message.channel.send(None, embed=out_content)
        return
    try:
        current_role = cmd.db.get_settings(message.guild.id, 'AutoRole')
    except KeyError:
        cmd.db.set_settings(message.guild.id, 'AutoRole', None)
        current_role = None
    if not args:
        if current_role:
            current_role = discord.utils.find(lambda x: x.id == current_role, message.guild.roles)
        if current_role:
            out_content = discord.Embed(type='rich', color=0x0099FF,
                                        title='ℹ Current Auto Role: ' + current_role.name)
            await message.channel.send(None, embed=out_content)
            return
        else:
            out_content = discord.Embed(type='rich', color=0x0099FF,
                                        title='ℹ No Auto Role Set')
            await message.channel.send(None, embed=out_content)
            return
    role_qry = ' '.join(args)
    role_qry_low = role_qry.lower()
    if role_qry_low == 'disable':
        cmd.db.set_settings(message.guild.id, 'AutoRole', None)
        out_content = discord.Embed(type='rich', color=0x66CC66,
                                    title='✅ Auto Role Disabled and Cleaned.')
        await message.channel.send(None, embed=out_content)
        return
    target_role = matching_role(message.guild, role_qry)
    if target_role:
        if current_role == target_role.id:
            out_content = discord.Embed(type='rich', color=0xFF9900, title='⚠ Error')
            out_content.add_field(name='Present Role', value='This Role is already the Auto Role for this server.')
            await message.channel.send(None, embed=out_content)
            return
        cmd.db.set_settings(message.guild.id, 'AutoRole', target_role.id)
        out_content = discord.Embed(type='rich', color=0x33CC33)
        out_content.add_field(name='✅ Success',
                              value='The role **' + role_qry + '** has been set as the Auto Role.')
    else:
        out_content = discord.Embed(type='rich', color=0xDB0000, title='❗ Error')
        out_content.add_field(name='Role Not Found', value='I have not found **' + role_qry + '** on this server.')
    await message.channel.send(None, embed=out_content)
