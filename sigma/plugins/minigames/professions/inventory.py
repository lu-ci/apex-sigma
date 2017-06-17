import discord
from sigma.core.utils import user_avatar
from humanfriendly.tables import format_pretty_table as boop

async def inventory(cmd, message, args):
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    inv = cmd.db.get_inv(target)
    if inv:
        size = len(inv)
        bordered_inv = inv[:20]
        headers = ['Item', 'Value']
        to_format = []
        for item in bordered_inv:
            to_format.append([item['name'], f'{item["value"]}'])
        output = boop(to_format,column_names=headers)
        response = discord.Embed(color=0xc16a4f)
        response.set_author(name=f'{target.name}#{target.discriminator}', icon_url=user_avatar(target))
        inv_text = f'Showing the first {len(bordered_inv)} items.'
        inv_text += f'\nYou have a total of {size} items in your inventory.'
        response.add_field(name='📦 Inventory Stats',
                           value=f'```py\n{inv_text}\n```')
        response.add_field(name='📋 Items Currently In It', value=f'```hs\n{output}\n```', inline=False)
    else:
        response = discord.Embed(color=0xc6e4b5, title='💸 Totally empty...')
    await message.channel.send(embed=response)
