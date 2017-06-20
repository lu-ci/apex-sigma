import discord
from config import Currency


async def inspect(cmd, message, args):
    if args:
        inv = cmd.db.get_inv(message.author)
        if inv:
            lookup = ' '.join(args)
            item = None
            for invitem in inv:
                if invitem['name'].lower() == lookup.lower():
                    item = invitem
                    break
            if item:
                connector = 'A'
                if item["rarity_name"][0].lower() in ['a', 'e', 'i', 'o', 'u']:
                    connector = 'An'
                item_info = f'{connector} **{item["rarity_name"].title()} {item["item_type"].title()}**'
                item_info += f'\nIt is valued at **{item["value"]} {Currency}**'
                response = discord.Embed(color=item['color'])
                response.add_field(name=f'{item["icon"]} {item["name"]}', value=f'{item_info}')
                response.add_field(name='Item Description', value=f'{item["description"]}', inline=False)
                response.set_footer(text=f'ItemID:{item["item_id"]}')
            else:
                response = discord.Embed(color=0x696969, title=f'🔍 I didn\'t find any {lookup} in your inventory.')
        else:
            response = discord.Embed(color=0xc6e4b5, title=f'💸 Your inventory is empty, {message.author.name}...')
    else:
        response = discord.Embed(color=0xDB0000, title='❗ You didn\'t input anything.')
    await message.channel.send(embed=response)
