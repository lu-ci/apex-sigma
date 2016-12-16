async def member_join_control(ev, member):
    server = member.server
    greet = ev.db.get_settings(server.id, 'Greet')
    if greet:
        greet_channel = ev.db.get_settings(server.id, 'GreetChannel')
        greet_message = ev.db.get_settings(server.id, 'GreetMessage')
        greet_message = greet_message.replace('%user_mention%', '<@' + member.id + '>').replace('%server_name%', server.name)
        if not greet_channel:
            greet_channel = server.default_channel.id
        target_channel = None
        for channel in server.channels:
            if channel.id == greet_channel:
                target_channel = channel
                break
        await ev.bot.send_message(target_channel, greet_message)
