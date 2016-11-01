import asyncio
from sigma.core.permission import check_man_chan


async def setchannelname(cmd, message, args):
    if not args:
        await cmd.reply(cmd.help())
        return
    else:
        if check_man_chan(message.author, message.channel):
            name_input = (' '.join(args)).replace(' ', '_').lower()
            name_pre = message.channel.name
            try:
                await cmd.bot.edit_channel(message.channel, name=name_input)
                response = await cmd.reply('The name of **' + name_pre + '** was set to **' + name_input + '**.')
            except Exception as e:
                response = await cmd.reply(str(e))
            await asyncio.sleep(10)
            await cmd.bot.delete_message(response)
        else:
            response = await cmd.reply('Only a user with the **Manage Channels** permission can use this command. :x:')
            await asyncio.sleep(10)
            await cmd.bot.delete_message(response)
