import discord
from sigma.core.rolecheck import matching_role, user_matching_role


async def togglerole(cmd, message, args):
    if not args:
        out_content = discord.Embed(type='rich', color=0xDB0000, title='❗ Error')
        out_content.add_field(name='Not Enough Arguments', value=cmd.help())
        await message.channel.send(None, embed=out_content)
        return
    else:
        role_qry = ' '.join(args).replace('"', '')
        self_roles = cmd.db.get_settings(message.guild.id, 'SelfRoles')
        self_role_id = None
        target_role = discord.utils.find(lambda x: x.name.lower() == role_qry.lower(), message.guild.roles)
        if target_role:
            for self_role in self_roles:
                if self_role == target_role.id:
                    self_role_id = target_role.id
                    break
        if target_role:
            if self_role_id:
                user_role_match = user_matching_role(message.author, target_role.name)
                if not user_role_match:
                    await message.author.add_roles(target_role)
                    embed = discord.Embed(title='✅ ' + target_role.name + ' has been added to you.',
                                          color=0x66cc66)
                else:
                    await message.author.remove_roles(target_role)
                    embed = discord.Embed(title='⚠ ' + target_role.name + ' has been removed from you.',
                                          color=0xFF9900)
                await message.channel.send(None, embed=embed)
            else:
                out_content = discord.Embed(type='rich', color=0xFF9900, title='⚠ Error')
                out_content.add_field(name='Role Not Found',
                                      value='I was unable to find that role in the list of self assignable roles for this server.')
                await message.channel.send(None, embed=out_content)
        else:
            out_content = discord.Embed(type='rich', color=0xFF9900, title='⚠ Error')
            out_content.add_field(name='Role Not Found',
                                  value='I was unable to find that role on this server.')
            await message.channel.send(None, embed=out_content)
