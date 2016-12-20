async def member_leave_control(ev, member):
    server = member.server
    bye = ev.db.get_settings(server.id, 'Bye')
    if bye:
        ev.db.add_stats('ByeCount')
        bye_channel = ev.db.get_settings(server.id, 'ByeChannel')
        bye_message = ev.db.get_settings(server.id, 'ByeMessage')
        bye_message = bye_message.replace('%user_mention%', member.name).replace('%server_name%', server.name)
        if not bye_channel:
            bye_channel = server.default_channel.id
        target_channel = None
        for channel in server.channels:
            if channel.id == bye_channel:
                target_channel = channel
                break
        await ev.bot.send_message(target_channel, bye_message)
