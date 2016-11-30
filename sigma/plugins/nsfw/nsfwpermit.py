import asyncio
from sigma.core.permission import check_admin, set_channel_nsfw


async def nsfwpermit(cmd, message, args):
    channel = message.channel

    if check_admin(message.author, channel):
        if set_channel_nsfw(cmd.db, channel.id):
            await cmd.bot.send_message(message.channel, 'The NSFW Module has been Enabled for <#' + channel.id + '>! :eggplant:')
        else:
            await cmd.bot.send_message(message.channel, 'Permission reverted to **Disabled**! :fire:')
    else:
        response = await cmd.bot.send_message(message.channel, 'Only an **Administrator** can manage permissions. :x:')
        await asyncio.sleep(10)
        await cmd.bot.delete_message(response)
