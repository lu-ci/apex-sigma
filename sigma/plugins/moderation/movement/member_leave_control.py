import discord


async def member_leave_control(ev, member):
    server = member.guild
    bye = ev.db.get_settings(server.id, 'Bye')
    if bye:
        ev.db.add_stats('ByeCount')
        bye_channel = ev.db.get_settings(server.id, 'ByeChannel')
        bye_message = ev.db.get_settings(server.id, 'ByeMessage')
        bye_message = bye_message.replace('%user_mention%', member.name).replace('%server_name%', server.name)
        if not bye_channel:
            target_channel = server.default_channe
        else:
            target_channel = discord.utils.find(lambda x: x.id == bye_channel, member.guild.channels)
        for channel in server.channels:
            if channel.id == bye_channel:
                target_channel = channel
                break
        await target_channel.send(bye_message)
