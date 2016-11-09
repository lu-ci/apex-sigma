from sigma.core.permission import check_man_msg
import asyncio


async def prune(cmd, message, args):
    channel = message.channel
    if check_man_msg(message.author, channel):
        try:
            if args[0]:
                count = int(args[0])
            else:
                count = 100
        except:
            count = 100
        try:
            if args[1]:
                def crit(m):
                    return m.author == message.mentions[0]
            else:
                crit = None
        except:
            crit = None
        try:
            await cmd.bot.purge_from(message.channel, limit=count, check=crit)
            response = await cmd.bot.send_message(message.channel, 'Done! :ok_hand:')
            await asyncio.sleep(10)
            await cmd.bot.delete_message(response)
        except Exception as e:
            cmd.log.error(e)
            await cmd.bot.send_message(message.channel, str(e))
    else:
        response = await cmd.bot.send_message(message.channel, 'Only a user with the **Manage Messages** privilege can use this command. :x:')
        await asyncio.sleep(10)
        await cmd.bot.delete_message(response)
