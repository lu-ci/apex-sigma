import discord
from sigma.core.permission import check_man_chan


async def movechannel(cmd, message, args):
    if not args:
        await message.channel.send(cmd.help())
        return
    else:
        if check_man_chan(message.author, message.channel):
            position = int(args[0])
            pos_pre = message.channel.position
            await cmd.bot.move_channel(message.channel, position)
            embed = discord.Embed(color=0x66CC66,
                                  title='✅ ' + message.channel.name + ' moved from ' + str(
                                      pos_pre) + ' to ' + str(position))
            await message.channel.send(None, embed=embed)
        else:
            embed = discord.Embed(type='rich', color=0xDB0000,
                                  title='⛔ Insufficient Permissions. Requires Manage Channels Permission Only.')
            await message.channel.send(None, embed=embed)
