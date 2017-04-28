import discord


async def decimaltohex(cmd, message, args):
    qry = ''.join(args)
    conv = hex(int(qry))
    conv = str(conv).split('x')[1].upper()
    embed = discord.Embed(color=0x1abc9c)
    embed.add_field(name='Converted Decimal To Hex', value='```\n' + conv + '\n```')
    await message.channel.send(None, embed=embed)
