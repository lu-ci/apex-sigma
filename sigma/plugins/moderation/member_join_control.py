async def member_join_control(ev, member):
    server = member.guild
    greet = ev.db.get_settings(server.id, 'Greet')
    greet_pm = ev.db.get_settings(server.id, 'GreetPM')
    try:
        autorole = ev.db.get_settings(server.id, 'AutoRole')
    except KeyError:
        ev.db.set_settings(server.id, 'AutoRole', None)
        autorole = None
    if greet:
        ev.db.add_stats('GreetCount')
        greet_message = ev.db.get_settings(server.id, 'GreetMessage')
        greet_message = greet_message.replace('%user_mention%', member.mention).replace('%server_name%',
                                                                                        server.name).replace(
            '%USER_MENTION%', member.mention).replace('%SERVER_NAME%', server.name.upper())
        if not greet_pm:
            greet_channel = ev.db.get_settings(server.id, 'GreetChannel')
            if not greet_channel:
                greet_channel = server.default_channel.id
            target_channel = None
            for channel in server.channels:
                if channel.id == greet_channel:
                    target_channel = channel
                    break
            await ev.bot.send_message(target_channel, greet_message)
        else:
            await ev.bot.send_message(member, greet_message)
    if autorole:
        target = None
        for role in member.guild.roles:
            if role.id == autorole:
                target = role
                break
        if target:
            await ev.bot.add_roles(member, target)
        else:
            await member.guild.default_channel.send(
                'I tried to assign the autorole to the user, but the AutoRole specified was not found so I reset the settings.')
            ev.db.set_settings(server.id, 'AutoRole', None)
