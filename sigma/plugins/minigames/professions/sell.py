import discord
from config import Currency
from .mechanics import get_item_by_name, get_item_by_id, get_all_items
from .mechanics import items

async def sell(cmd, message, args):
    if not items:
        get_all_items('fish', cmd.resource('data'))
    if args:
        inv = cmd.db.get_inv(message.author)
        if inv:
            lookup = ' '.join(args)
            if lookup == 'all':
                value = 0
                count = 0
                for invitem in inv:
                    item_ob_id = get_item_by_id(invitem['item_file_id'])
                    value += item_ob_id.value
                    count += 1
                    cmd.db.inv_del(message.author, invitem['item_id'])
                cmd.db.add_points(message.author.guild, message.author, value)
                response = discord.Embed(color=0xc6e4b5, title=f'💶 You sold {count} items for {value} {Currency}.')
            else:
                item_o = get_item_by_name(lookup)
                if item_o:
                    item = cmd.db.get_inv_item(message.author, item_o.item_file_id)
                else:
                    item = None
                if item:
                    value = item_o.value
                    cmd.db.add_points(message.author.guild, message.author, value)
                    cmd.db.inv_del(message.author, item['item_id'])
                    response = discord.Embed(color=0xc6e4b5,
                                             title=f'💶 You sold the {item_o.name} for {value} {Currency}.')
                else:
                    response = discord.Embed(color=0x696969, title=f'🔍 I didn\'t find any {lookup} in your inventory.')
        else:
            response = discord.Embed(color=0xc6e4b5, title=f'💸 Your inventory is empty, {message.author.name}...')
    else:
        response = discord.Embed(color=0xDB0000, title='❗ You didn\'t input anything.')
    await message.channel.send(embed=response)
