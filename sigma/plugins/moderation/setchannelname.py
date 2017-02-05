import discord
from sigma.core.permission import check_man_chan


async def setchannelname(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    else:
        if check_man_chan(message.author, message.channel):
            name_input = (' '.join(args)).replace(' ', '_').lower()
            name_pre = message.channel.name
            await cmd.bot.edit_channel(message.channel, name=name_input)
            embed = discord.Embed(color=0x66CC66, title='#' + name_pre + ' renamed to #' + name_input)
            await cmd.bot.send_message(message.channel, None, embed=embed)
        else:
            out_content = discord.Embed(color=0xDB0000,
                                        title=':no_entry: Insufficient Permissions. Manage Channels Permission Required.')
            await cmd.bot.send_message(message.channel, None, embed=out_content)
