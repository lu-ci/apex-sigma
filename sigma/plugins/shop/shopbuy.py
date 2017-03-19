import discord
from sigma.core.rolecheck import matching_role, user_matching_role


async def shopbuy(cmd, message, args):
    if not args:
        status = discord.Embed(type='rich', color=0xDB0000,
                               title='❗ Insufficient Arguments.')
        await cmd.bot.send_message(message.channel, None, embed=status)
        return
    role_name = ' '.join(args)
    item_list = cmd.db.get_settings(message.server.id, 'ShopItems')
    found = False
    for item in item_list:
        if item['RoleName'].lower() == role_name.lower():
            found = True
            price = int(item['Price'])
            role = matching_role(message.server, role_name)
            if not user_matching_role(message.author, role_name):
                user_points = cmd.db.get_points(message.server, message.author)
                if user_points >= price:
                    await cmd.bot.add_roles(message.author, role)
                    cmd.db.take_points(message.server, message.author, price)
                    status = discord.Embed(type='rich', color=0x66cc66,
                                           title='✅ You bought ' + role.name + ' .')
                else:
                    status = discord.Embed(type='rich', color=0xFF9900,
                                           title='⚠ You can\'t afford it.')
                await cmd.bot.send_message(message.channel, None, embed=status)
            else:
                status = discord.Embed(type='rich', color=0xFF9900,
                                       title='⚠ You already have this role.')
                await cmd.bot.send_message(message.channel, None, embed=status)
            break
    if not found:
        status = discord.Embed(type='rich', color=0xDB0000,
                               title='❗ Couldn\'t find  this in the shop.')
        await cmd.bot.send_message(message.channel, None, embed=status)
