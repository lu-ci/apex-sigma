from sigma.core.permission import check_admin


async def sfiexec(ev, message, args):
    if 'discord.gg' in message.content:
        if check_admin(message.author, message.channel):
            return
        else:
            n = 0
            search_data = {
                'ServerID': message.server.id
            }
            search = ev.db.find('ServerFilterInvites', search_data)
            active = False
            for result in search:
                n += 1
                try:
                    active = result['Active']
                except:
                    pass
            if n == 0:
                return
            else:
                if active:
                    await ev.bot.delete_message(message)
                else:
                    return
