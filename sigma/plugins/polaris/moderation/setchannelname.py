import asyncio
from sigma.core.permission import check_man_chan


async def setchannelname(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    else:
        if check_man_chan(message.author, message.channel):
            name_input = (' '.join(args)).replace(' ', '_').lower()
            name_pre = message.channel.name
            try:
                await cmd.bot.edit_channel(message.channel, name=name_input)
                response = await cmd.bot.send_message(message.channel, 'The name of **' + name_pre + '** was set to **' + name_input + '**.')
            except Exception as e:
                response = await cmd.bot.send_message(message.channel, str(e))
            await asyncio.sleep(10)
            await cmd.bot.delete_message(response)
        else:
            response = await cmd.bot.send_message(message.channel, 'Only a user with the **Manage Channels** permission can use this command. :x:')
            await asyncio.sleep(10)
            await cmd.bot.delete_message(response)
