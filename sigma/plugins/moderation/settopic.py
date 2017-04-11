import discord
from sigma.core.permission import check_man_chan


async def settopic(cmd, message, args):
    if not args:
        await message.channel.send(cmd.help())
        return
    else:
        if check_man_chan(message.author, message.channel):
            topic = ' '.join(args)
            await message.channel.edit(topic=topic)
            embed = discord.Embed(color=0x66CC66)
            embed.add_field(name='✅ #' + message.channel.name + ' topic changed to:',
                            value='```\n' + topic + '\n```')
            await message.channel.send(None, embed=embed)
        else:
            out_content = discord.Embed(type='rich', color=0xDB0000,
                                        title='⛔ Insufficient Permissions. Manage Channels Permission Required.')
            await message.channel.send(None, embed=out_content)
