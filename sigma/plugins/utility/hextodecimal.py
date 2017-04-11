import discord


async def hextodecimal(cmd, message, args):
    qry = ''.join(args)
    conv = int(qry, 16)
    embed = discord.Embed(color=0x1abc9c)
    embed.add_field(name='Converted Hex To Decimal', value='```\n' + str(conv) + '\n```')
    await message.channel.send(None, embed=embed)
