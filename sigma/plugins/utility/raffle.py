import asyncio
import random
from sigma.core.permission import check_admin

async def raffle(cmd, message, args):
    if check_admin(message.author, message.channel):
        user_list = []
        for member in message.server.members:
            status = str(member.status)
            if status == 'offline':
                pass
            else:
                user_list.append(member.id)
        winner = random.choice(user_list)
        await cmd.bot.send_message(message.channel, 'The Winner Is <@' + winner + '>!\nCongratulations!')
    else:
        response = await cmd.bot.send_message(message.channel, 'Only a server **Administrator** can use this command. :x:')
        await asyncio.sleep(10)
        await cmd.bot.delete_message(response)
