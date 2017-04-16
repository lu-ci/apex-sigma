import discord


async def inventory(cmd, message, args):
    inv = cmd.db.get_inv(message.author)
    if inv:
        output = ''
        for item in inv:
            output += f'\n{item["name"]}'
        response = discord.Embed(color=0x1abc9c)
        response.add_field(name='Your Inventory', value=f'```\n{output}\n```')
    else:
        response = discord.Embed(color=0x1abc9c, title='Totally empty...')
    await message.channel.send(embed=response)
