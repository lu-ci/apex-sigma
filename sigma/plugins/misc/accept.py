import asyncio


async def accept(ev, message, args):
    if message.channel.id == '225375071349243904':
        if message.author == ev.bot.user:
            return
        else:
            await ev.bot.delete_message(message)
            if message.content == '>>accept':
                for role_x in message.server.roles:
                    if role_x.name == 'Crabigator\'s Pet':
                        await ev.bot.add_roles(message.author, role_x)
                        break
                for role_y in message.server.roles:
                    if role_y.name == 'Guest':
                        await ev.bot.remove_roles(message.author, role_y)
                        break
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
