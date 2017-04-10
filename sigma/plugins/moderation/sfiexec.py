from sigma.core.permission import check_admin


async def sfiexec(ev, message, args):
    if message.guild:
        if 'discord.gg' in message.content:
            if check_admin(message.author, message.channel):
                return
            else:
                active = ev.db.get_settings(message.guild.id, 'BlockInvites')
                if active:
                    try:
                        await ev.bot.delete_message(message)
                    except Exception as e:
                        ev.log.error(e)
                else:
                    return
