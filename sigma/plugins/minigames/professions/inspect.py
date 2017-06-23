import discord
from config import Currency
from .mechanics import get_item_by_name, items, get_all_items


async def inspect(cmd, message, args):
    if not items:
        get_all_items('fish', cmd.resource('data'))
    if args:
        inv = cmd.db.get_inv(message.author)
        if inv:
            lookup = ' '.join(args)
            item_o = get_item_by_name(lookup)
            if item_o:
                item = cmd.db.get_inv_item(message.author, item_o.item_file_id)
            else:
                item = None
            if item:
                connector = 'A'
                if item_o.rarity_name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                    connector = 'An'
                item_info = f'{connector} **{item_o.rarity_name.title()} {item_o.item_type.title()}**'
                item_info += f'\nIt is valued at **{item_o.value} {Currency}**'
                response = discord.Embed(color=item_o.color)
                response.add_field(name=f'{item_o.icon} {item_o.name}', value=f'{item_info}')
                response.add_field(name='Item Description', value=f'{item_o.description}', inline=False)
                response.set_footer(text=f'ItemID: {item["item_id"]}')
            else:
                response = discord.Embed(color=0x696969, title=f'🔍 I didn\'t find any {lookup} in your inventory.')
        else:
            response = discord.Embed(color=0xc6e4b5, title=f'💸 Your inventory is empty, {message.author.name}...')
    else:
        response = discord.Embed(color=0xDB0000, title='❗ You didn\'t input anything.')
    await message.channel.send(embed=response)
