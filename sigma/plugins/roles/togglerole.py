import discord
from sigma.core.rolecheck import matching_role, user_matching_role


async def togglerole(cmd, message, args):
    if not args:
        out_content = discord.Embed(type='rich', color=0xDB0000, title='❗ Error')
        out_content.add_field(name='Not Enough Arguments', value=cmd.help())
        await message.channel.send(None, embed=out_content)
        return
    else:
        role_qry = ' '.join(args)
        self_roles = cmd.db.get_settings(message.guild.id, 'SelfRoles')
        role_name = None
        for role in self_roles:
            if role.lower() == role_qry.lower():
                role_name = role
                break
        if role_name:
            user_role_match = user_matching_role(message.author, role_name)
            if not user_role_match:
                target_role = matching_role(message.guild, role_name)
                await cmd.bot.add_roles(message.author, target_role)
                embed = discord.Embed(title='✅ ' + role_name + ' has been added to you.',
                                      color=0x66cc66)
            else:
                target_role = user_role_match
                await cmd.bot.remove_roles(message.author, target_role)
                embed = discord.Embed(title='⚠ ' + role_name + ' has been removed from you.',
                                      color=0xFF9900)
            await message.channel.send(None, embed=embed)
        else:
            out_content = discord.Embed(type='rich', color=0xFF9900, title='⚠ Error')
            out_content.add_field(name='Role Not Found',
                                  value='I was unable to find that role in the list of self assignable roles for this server.')
            await message.channel.send(None, embed=out_content)
