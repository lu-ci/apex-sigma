import asyncio
from config import permitted_id


async def setname(cmd, message, args):
    if message.author.id in permitted_id:
        if not args:
            await cmd.bot.send_message(message.channel, cmd.help())
            return
        else:
            username = ' '.join(args)
            await cmd.bot.edit_profile(username=username)
            await cmd.bot.send_message(message.channel, 'Username changed to **' + username + '**.')
    else:
        response = await cmd.bot.send_message(message.channel, 'Unpermitted. :x:')
        await asyncio.sleep(10)
        await cmd.bot.delete_message(response)
