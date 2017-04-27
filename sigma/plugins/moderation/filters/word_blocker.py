from sigma.core.permission import check_admin


async def word_blocker(ev, message, args):
    if message.guild:
        if not check_admin(message.author, message.channel):
            try:
                blacklist = ev.db.get_settings(message.guild.id, 'BlockedWords')
            except:
                ev.db.set_settings(message.guild.id, 'BlockedWords', [])
                blacklist = []
            for word in args:
                if word in blacklist:
                    await message.delete()
                    break
