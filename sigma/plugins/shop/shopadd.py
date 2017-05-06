import discord
from sigma.core.permission import check_admin
from sigma.core.rolecheck import matching_role


async def shopadd(cmd, message, args):
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
    if len(args) < 2:
        status = discord.Embed(type='rich', color=0xDB0000,
                               title='❗ Insufficient Arguments.')
        await message.channel.send(None, embed=status)
        return
    price = abs(int(args[0]))
    role_name = ' '.join(args[1:])
    rtrl = matching_role(message.guild, role_name)
    if not rtrl:
        status = discord.Embed(type='rich', color=0xDB0000,
                               title='❗ The Role ' + role_name + ' was not found on the server.')
        await message.channel.send(None, embed=status)
        return
    role_data = {
        'RoleName': rtrl.name,
        'RoleID': rtrl.id,
        'RoleColor': str(rtrl.color),
        'Price': price
    }
    shop_list = cmd.db.get_settings(message.guild.id, 'ShopItems')
    if not shop_list:
        cmd.db.set_settings(message.guild.id, 'ShopItems', [])
        shop_list = []
    found = False
    for item in shop_list:
        if item['RoleID'] == rtrl.id:
            found = True
            status = discord.Embed(type='rich', color=0xFF9900,
                                   title='⚠ The Role ' + rtrl.name + ' is already in the shop.')
            await message.channel.send(None, embed=status)
            break
    if found == 0:
        shop_list.append(role_data)
        cmd.db.set_settings(message.guild.id, 'ShopItems', shop_list)
        status = discord.Embed(type='rich', color=0x66CC66,
                               title='✅ ' + rtrl.name + ' has been added to the shop.')
        await message.channel.send(None, embed=status)
