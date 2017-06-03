async def mute_check(ev, message, args):
    if message.guild:
        try:
            mute_list = ev.db.get_settings(message.guild.id, 'MutedUsers')
        except:
            mute_list = []
        if message.author.id in mute_list:
            try:
                await message.delete(reason='User is text muted.')
            except:
                pass
