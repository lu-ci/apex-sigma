from sigma.core.permission import check_admin


async def word_edit_blocker(ev, before, after):
    if after.guild:
        if not check_admin(after.author, after.channel):
            try:
                blacklist = ev.db.get_settings(after.guild.id, 'BlockedWords')
            except:
                ev.db.set_settings(after.guild.id, 'BlockedWords', [])
                blacklist = []
            args = after.content.split(' ')
            for word in args:
                if word in blacklist:
                    await after.delete()
                    break
