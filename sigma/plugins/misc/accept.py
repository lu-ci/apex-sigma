import asyncio


async def accept(ev, message, args):
    if message.channel.id == '225375071349243904':
        if message.author == ev.bot.user:
            return
        else:
            await ev.bot.delete_message(message)
            if message.content == '>>accept':
                for role in message.server.roles:
                    if role.name == 'Crabigator\'s Pet':
                        await ev.bot.add_roles(message.author, role)
                        break
            elif message.content == '>>decline':
                response = await ev.reply(
                    'We are sorry to hear that.\nYou will be removed from the server shortly.\nBon voyage~')
                await asyncio.sleep(10)
                await ev.bot.kick(message.author)
                await ev.bot.delete_message(response)
