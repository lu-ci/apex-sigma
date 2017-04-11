import discord
from sigma.core.permission import check_man_roles
from sigma.core.rolecheck import matching_role


async def destroyrole(cmd, message, args):
    if not check_man_roles(message.author, message.channel):
        out_content = discord.Embed(type='rich', color=0xDB0000,
                                    title='⛔ Insufficient Permissions. Server Admin Only.')
        await message.channel.send(None, embed=out_content)
        return
    if not args:
        out_content = discord.Embed(type='rich', color=0xDB0000, title='❗ Error')
        out_content.add_field(name='Not Enough Arguments', value=cmd.help())
        await message.channel.send(None, embed=out_content)
        return
    role_qry = ' '.join(args)
    target_role = matching_role(message.guild, role_qry)
    if not target_role:
        out_content = discord.Embed(type='rich', color=0xFF9900, title='❗ Error')
        out_content.add_field(name='Role Not Found', value='I was unable to find **' + role_qry + '** on this server.')
        await message.channel.send(None, embed=out_content)
    else:
        await target_role.delete()
        out_content = discord.Embed(type='rich', color=0x66cc66,
                                    title='✅ Role ' + role_qry + ' destroyed.')
        await message.channel.send(None, embed=out_content)
