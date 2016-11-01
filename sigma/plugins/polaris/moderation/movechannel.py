import asyncio
from sigma.core.permission import check_man_chan


async def movechannel(cmd, message, args):
    if not args:
        await cmd.reply(cmd.help())
        return
    else:
        if check_man_chan(message.author, message.channel):
            position = int(args[0])
            pos_pre = message.channel.position
            try:
                await cmd.bot.move_channel(message.channel, position)
                response = await cmd.reply(
                    'Channel **' + message.channel.name + '** was moved from **' + str(pos_pre) + '** to **' + str(
                        position) + '**.')
            except Exception as e:
                response = await cmd.reply(str(e))
            await asyncio.sleep(10)
            await cmd.bot.delete_message(response)
        else:
            response = await cmd.reply('Only a user with the **Manage Channels** permission can use this command. :x:')
            await asyncio.sleep(10)
            await cmd.bot.delete_message(response)
