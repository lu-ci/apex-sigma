from sigma.core.permission import check_ban
import asyncio


async def ban(cmd, message, args):
    channel = message.channel
    if args[0]:
        user_q = message.mentions[0]
        if message.author is not user_q:
            if check_ban(message.author, channel):
                try:
                    await cmd.bot.ban(user_q)
                    await cmd.reply('User **' + user_q.name + '** has been banned.')
                except Exception as e:
                    cmd.log.error(e)
                    await cmd.reply(str(e))
            else:
                response = await cmd.reply('Only a user with **Ban** privileges can use this command. :x:')
                await asyncio.sleep(10)
                await cmd.bot.delete_message(response)
        else:
            await cmd.reply(cmd.help())
    else:
        await cmd.reply(cmd.help())
