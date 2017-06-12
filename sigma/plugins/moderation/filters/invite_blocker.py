from sigma.core.permission import check_admin


async def invite_blocker(ev, message, args):
    if message.guild:
        if not check_admin(message.author, message.channel):
            if 'discord.gg/' or 'discordapp.com/invite/' in message.content:
                active = ev.db.get_settings(message.guild.id, 'BlockInvites')
                if active:
                    await message.delete()
