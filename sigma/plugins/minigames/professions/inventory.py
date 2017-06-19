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
        headers = ['Item', 'Type', 'Value']
        to_format = []
        for item in inv:
            to_format.append([item['name'], item['item_type'],f'{item["value"]}'])
        output = boop(to_format,column_names=headers)
        response = discord.Embed(color=0xc16a4f)
        response.set_author(name=f'{target.name}#{target.discriminator}', icon_url=user_avatar(target))
        inv_text = f'You have a total of {len(inv)} items in your inventory.'
        response.add_field(name='📦 Inventory Stats',
                           value=f'```py\n{inv_text}\n```')
        response.add_field(name='📋 Items Currently In It', value=f'```hs\n{output}\n```', inline=False)
    else:
        response = discord.Embed(color=0xc6e4b5, title='💸 Totally empty...')
    await message.channel.send(embed=response)
