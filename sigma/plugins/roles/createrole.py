import discord
from sigma.core.permission import check_man_roles
from sigma.core.rolecheck import matching_role


async def createrole(cmd, message, args):
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
    exists = matching_role(message.guild, role_qry)
    if exists:
        out_content = discord.Embed(type='rich', color=0xFF9900, title='⚠ Error')
        out_content.add_field(name='Role Exists', value='A role with the name **' + role_qry + '** already exists.')
        await message.channel.send(None, embed=out_content)
    else:
        await message.guild.create_role(name=role_qry)
        out_content = discord.Embed(type='rich', color=0x33CC33,
                                    title='✅ Role ' + role_qry + ' created.')
        await message.channel.send(None, embed=out_content)
