from sigma.core.permission import check_kick
import asyncio


async def kick(cmd, message, args):
    channel = message.channel
    if args[0]:
        user_q = message.mentions[0]
        if message.author is not user_q:
            if check_kick(message.author, channel):
                try:
                    await cmd.bot.kick(user_q)
                    await cmd.reply('User **' + user_q.name + '** has been kicked.')
                except Exception as e:
                    cmd.log.error(e)
                    await cmd.reply(str(e))
            else:
                response = await cmd.reply('Only a user with **Kick** privileges can use this command. :x:')
                await asyncio.sleep(10)
                await cmd.bot.delete_message(response)
