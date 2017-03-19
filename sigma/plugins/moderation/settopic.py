import discord
from sigma.core.permission import check_man_chan


async def settopic(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    else:
        if check_man_chan(message.author, message.channel):
            topic = ' '.join(args)
            await cmd.bot.edit_channel(message.channel, topic=topic)
            embed = discord.Embed(color=0x66CC66)
            embed.add_field(name='✅ #' + message.channel.name + ' topic changed to:',
                            value='```\n' + topic + '\n```')
            await cmd.bot.send_message(message.channel, None, embed=embed)
        else:
            out_content = discord.Embed(type='rich', color=0xDB0000,
                                        title=':no_entry: Insufficient Permissions. Manage Channels Permission Required.')
            await cmd.bot.send_message(message.channel, None, embed=out_content)
