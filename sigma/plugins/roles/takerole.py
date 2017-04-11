from sigma.core.permission import check_man_roles
from sigma.core.rolecheck import matching_role, user_matching_role
import discord


async def takerole(cmd, message, args):
    if not check_man_roles(message.author, message.channel):
        out_content = discord.Embed(type='rich', color=0xDB0000,
                                    title='⛔ Insufficient Permissions. Server Admin Only.')
        await message.channel.send(None, embed=out_content)
        return
    if len(args) < 2:
        out_content = discord.Embed(type='rich', color=0xDB0000, title='❗ Error')
        out_content.add_field(name='Missing Arguments', value=cmd.help())
        await message.channel.send(None, embed=out_content)
        return
    if not message.mentions:
        out_content = discord.Embed(type='rich', color=0xDB0000, title='❗ Error')
        out_content.add_field(name='Missing Target User', value=cmd.help())
        await message.channel.send(None, embed=out_content)
        return
    role_qry = ' '.join(args[1:])
    target_role = matching_role(message.guild, role_qry)
    target_user = message.mentions[0]
    user_contained_role = user_matching_role(target_user, role_qry)
    if not target_role:
        out_content = discord.Embed(type='rich', color=0xFF9900, title='❗ Error')
        out_content.add_field(name='Role Not Found', value='I was unable to find **' + role_qry + '** on this server.')
        await message.channel.send(None, embed=out_content)
    else:
        if user_contained_role:
            await target_user.remove_roles(target_role)
            out_content = discord.Embed(type='rich', color=0x66cc66,
                                        title='✅ Role ' + role_qry + ' removed from **' + target_user.name + '**.')
            await message.channel.send(None, embed=out_content)
        else:
            out_content = discord.Embed(type='rich', color=0xFF9900, title='❗ Error')
            out_content.add_field(name='User Missing Role',
                                  value='I was unable to find **' + role_qry + '** in ' + target_user.name + '\'s roles.')
            await message.channel.send(None, embed=out_content)
