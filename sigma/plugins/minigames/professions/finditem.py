import discord
from config import Currency
from .mechanics import get_all_items, get_item_by_name

async def finditem(cmd, message, args):
    if args:
        if len(args) >= 2:
            item_type = args[0].lower()
            lookup = ' '.join(args[1:])
            try:
                inv = get_all_items(item_type, cmd.resource('data'))
            except KeyError:
                inv = None
            if inv:
                item = get_item_by_name(lookup)
                if item:
                    connector = 'A'
                    if item.rarity_name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                        connector = 'An'
                    item_info = f'{connector} **{item.rarity_name.title()} {item.item_type.title()}**'
                    item_info += f'\nIt is valued at **{item.value} {Currency}**'
                    response = discord.Embed(color=item.color)
                    response.add_field(name=f'{item.icon} {item.name}', value=f'{item_info}')
                    response.add_field(name='Item Description', value=f'{item.description}', inline=False)
                else:
                    response = discord.Embed(color=0x696969, title=f'🔍 I didn\'t find any {lookup} in your inventory.')
            else:
                response = discord.Embed(color=0x696969, title=f'🔍 I didn\'t find the {item_type} category.')
        else:
            response = discord.Embed(color=0xDB0000, title='❗ Not enough arguments..')
    else:
        response = discord.Embed(color=0xDB0000, title='❗ You didn\'t input anything.')
    await message.channel.send(embed=response)
