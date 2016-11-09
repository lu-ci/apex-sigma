import asyncio
from sigma.core.permission import check_man_chan


async def settopic(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    else:
        if check_man_chan(message.author, message.channel):
            topic = ' '.join(args)
            try:
                await cmd.bot.edit_channel(message.channel, topic=topic)
                response = await cmd.bot.send_message(message.channel, 
                    'The topic of **' + message.channel.name + '** was set to ```' + topic + '```')
            except Exception as e:
                response = await cmd.bot.send_message(message.channel, str(e))
            await asyncio.sleep(10)
            await cmd.bot.delete_message(response)
        else:
            response = await cmd.bot.send_message(message.channel, 'Only a user with the **Manage Channels** permission can use this command. :x:')
            await asyncio.sleep(10)
            await cmd.bot.delete_message(response)
