import discord
from sigma.core.permission import check_admin
from sigma.core.rolecheck import matching_role


async def shopremove(cmd, message, args):
    if not check_admin(message.author, message.channel):
        status = discord.Embed(type='rich', color=0xDB0000,
                               title='⛔ Insufficient Permissions. Server Admin Only.')
        await message.channel.send(None, embed=status)
        return
    if not args:
        status = discord.Embed(type='rich', color=0xDB0000,
                               title='❗ Insufficient Arguments.')
        await message.channel.send(None, embed=status)
        return
    role_name = ' '.join(args)
    rtrl = matching_role(message.guild, role_name)
    shop_list = cmd.db.get_settings(message.guild.id, 'ShopItems')
    if not rtrl:
        status = discord.Embed(type='rich', color=0xDB0000,
                               title='❗ The Role ' + role_name + ' was not found on the server.')
        for item in shop_list:
            if item['RoleName'].lower() == role_name.lower():
                shop_list.remove(item)
                status.set_footer(text='It was found in the shop however, and removed.')
                cmd.db.set_settings(message.guild.id, 'ShopItems', shop_list)
                break
        await message.channel.send(None, embed=status)
        return
    else:
        found = False
        for item in shop_list:
            if item['RoleID'] == rtrl.id:
                found = True
                shop_list.remove(item)
                cmd.db.set_settings(message.guild.id, 'ShopItems', shop_list)
                status = discord.Embed(type='rich', color=0x66CC66,
                                       title='✅ ' + rtrl.name + ' has been removed from the shop.')
                await message.channel.send(None, embed=status)
                break
        if not found:
            status = discord.Embed(type='rich', color=0xFF9900,
                                   title='⚠ The Role ' + rtrl.name + ' is not in the shop.')
            await message.channel.send(None, embed=status)
