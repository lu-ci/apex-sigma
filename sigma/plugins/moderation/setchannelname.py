import discord
from sigma.core.permission import check_man_chan


async def setchannelname(cmd, message, args):
    if not args:
        await message.channel.send(cmd.help())
        return
    else:
        if check_man_chan(message.author, message.channel):
            name_input = (' '.join(args)).replace(' ', '_').lower()
            name_pre = message.channel.name
            await message.channel.edit(name=name_input)
            embed = discord.Embed(color=0x66CC66, title='#' + name_pre + ' renamed to #' + name_input)
            await message.channel.send(None, embed=embed)
        else:
            out_content = discord.Embed(color=0xDB0000,
                                        title='⛔ Insufficient Permissions. Manage Channels Permission Required.')
            await message.channel.send(None, embed=out_content)
