import discord


async def shoplist(cmd, message, args):
    shop_list = cmd.db.get_settings(message.guild.id, 'ShopItems')
    if not shop_list:
        cmd.db.set_settings(message.guild.id, 'ShopItems', [])
        shop_list = []
    if len(shop_list) == 0:
        embed = discord.Embed(color=0xFF9900, title='⚠ The Shop Is Empty.')
    else:
        embed = discord.Embed(color=0x1abc9c, title=':gem: ' + message.guild.name + '\'s Role Shop')
        role_out = ''

        def pricecheck(itm):
            return int(itm['Price'])

        shop_list = sorted(shop_list, key=pricecheck)
        for item in shop_list:
            role_out += f"\n```yml\n\'{item['RoleName']}\'\n - {item['Price']}\n```"
        embed.add_field(name='Items and Prices', value=role_out)
    await message.channel.send(None, embed=embed)
