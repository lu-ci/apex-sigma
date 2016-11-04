from sigma.core.permission import check_ban
import asyncio


async def unban(cmd, message, args):
    channel = message.channel
    if args:
        user_q = args[0]
        if message.author is not user_q:
            if check_ban(message.author, channel):
                try:
                    ban_list = await cmd.bot.get_bans(message.server)
                    target_user = None
                    for user in ban_list:
                        if user.name.lower() == user_q.lower():
                            target_user = user
                            break
                    if target_user:
                        await cmd.bot.unban(message.server, target_user)
                        await cmd.reply('User **' + user_q + '** has been unbanned.')
                    else:
                        await cmd.reply('A user with that name was not found in the server ban list.')
                except SyntaxError as e:
                    cmd.log.error(e)
                    await cmd.reply(str(e))
            else:
                response = await cmd.reply('Only a user with **Ban** privileges can use this command. :x:')
                await asyncio.sleep(10)
                await cmd.bot.delete_message(response)
    else:
        await cmd.reply(cmd.help())
