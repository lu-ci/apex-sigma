import asyncio


async def accept(ev, message, args):
    if message.channel.id == '225375071349243904':
        if message.author == ev.bot.user:
            return
        else:
            await ev.bot.delete_message(message)
            give_role = None
            take_role = None
            for role in message.server.roles:
                if role.name == 'Crabigator\'s Pet':
                    give_role = role
                elif role.name == 'Guest':
                    take_role = role
                else:
                    pass
            if not give_role and not take_role:
                return
            if message.content == '>>accept':
                await ev.bot.add_roles(message.author, give_role)
                await asyncio.sleep(3)
                await ev.bot.remove_roles(message.author, take_role)
                for channel in message.server.channels:
                    if channel.is_default:
                        await ev.bot.send_message(channel,
                                                  'Hello <@' + message.author.id + '>! Welcome to the WaniKani Community Discord Server! If you wanna chat, feel bored, need help with your Nihongo or whatever crosses your mind, you are welcome to chat about it here~ If you encounter any problems be sure to say so to a moderator! The pinned messages in each channel will have some info as well\nようこそ！もし日本語でしゃべりたければ、音声チャネルにご参加ください！')
            elif message.content == '>>decline':
                response = await ev.reply(
                    'We are sorry to hear that.\nYou will be removed from the server shortly.\nBon voyage~')
                await asyncio.sleep(10)
                await ev.bot.kick(message.author)
                await ev.bot.delete_message(response)
