import discord
from config import Currency


async def sell(cmd, message, args):
    if args:
        inv = cmd.db.get_inv(message.author)
        if inv:
            lookup = ' '.join(args)
            if lookup == 'all':
                value = 0
                count = 0
                for invitem in inv:
                    value += invitem['value']
                    count += 1
                    cmd.db.inv_del(message.author, invitem['ItemID'])
                cmd.db.add_points(message.author.guild, message.author, value)
                response = discord.Embed(color=0, title=f'💶 You sold {count} items for {value} {Currency}.')
            else:
                item = None
                for invitem in inv:
                    if invitem['name'].lower() == lookup.lower():
                        item = invitem
                        break
                if item:
                    value = item['value']
                    cmd.db.add_points(message.author.guild, message.author, value)
                    cmd.db.inv_del(message.author, item['ItemID'])
                    response = discord.Embed(color=0xc6e4b5,
                                             title=f'💶 You sold the {item["name"]} for {value} {Currency}.')
                else:
                    response = discord.Embed(color=0x696969, title=f'🔍 I didn\'t find any {lookup} in your inventory.')
        else:
            response = discord.Embed(color=0x1abc9c, title=f'💸 Your inventory is empty, {message.author.name}...')
    else:
        response = discord.Embed(color=0xDB0000, title='❗ You didn\'t input anything.')
    await message.channel.send(embed=response)
