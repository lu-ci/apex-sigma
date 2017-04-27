from sigma.core.permission import check_admin


async def invite_blocker(ev, message, args):
    if message.guild:
        if not check_admin(message.author, message.channel):
            if 'discord.gg' in message.content:
                active = ev.db.get_settings(message.guild.id, 'BlockInvites')
                if active:
                    try:
                        await message.delete()
                    except Exception as e:
                        ev.log.error(e)
                else:
                    return
