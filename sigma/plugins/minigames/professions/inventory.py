import discord
from config import Currency
from sigma.core.utils import user_avatar
from humanfriendly.tables import format_pretty_table as boop
from .mechanics import get_item_by_id, items, get_all_items


async def inventory(cmd, message, args):
    if not items:
        get_all_items('fish', cmd.resource('data'))
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    page_number = 1
    if args:
        try:
            page_number = abs(int(args[0]))
            if page_number == 0:
                page_number = 1
        except TypeError:
            page_number = 0
        except ValueError:
            page_number = 0
    start_range = (page_number - 1) * 10
    end_range = page_number * 10
    inv = cmd.db.get_inv(target)
    total_inv = len(inv)
    item_o_list = []
    for item in inv:
        item_o = get_item_by_id(item['item_file_id'])
        item_o_list.append(item_o)
    item_o_list = sorted(item_o_list, key=lambda x: x.rarity, reverse=True)
    inv = item_o_list[start_range:end_range]
    if inv:
        headers = ['Type', 'Item', 'Value', 'Rarity']
        to_format = []
        total_value = 0
        for item_o_item in inv:
            to_format.append(
                [item_o_item.item_type, item_o_item.name, f'{item_o_item.value}', f'{item_o_item.rarity_name.title()}'])
        for item_o_item in item_o_list:
            total_value += item_o_item.value
        output = boop(to_format, column_names=headers)
        response = discord.Embed(color=0xc16a4f)
        response.set_author(name=f'{target.name}#{target.discriminator}', icon_url=user_avatar(target))
        inv_text = f'Showing {len(inv)}/{total_inv} items in your inventory.'
        inv_text += f'\nTotal value of your inventory is {total_value} {Currency}.'
        response.add_field(name='📦 Inventory Stats',
                           value=f'```py\n{inv_text}\n```')
        response.add_field(name=f'📋 Items Currently On Page {page_number}', value=f'```hs\n{output}\n```',
                           inline=False)
    else:
        response = discord.Embed(color=0xc6e4b5, title='💸 Totally empty...')
    await message.channel.send(embed=response)
