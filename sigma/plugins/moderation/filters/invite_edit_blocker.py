from sigma.core.permission import check_admin


async def invite_edit_blocker(ev, before, after):
    if after.guild:
        if not check_admin(after.author, after.channel):
            if 'discord.gg/' or 'discordapp.com/invite/' in after.content:
                active = ev.db.get_settings(after.guild.id, 'BlockInvites')
                if active:
                    await after.delete()
