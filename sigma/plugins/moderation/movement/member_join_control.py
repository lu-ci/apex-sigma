import asyncio
import discord


async def member_join_control(ev, member):
    server = member.guild
    greet = ev.db.get_settings(server.id, 'Greet')
    greet_pm = ev.db.get_settings(server.id, 'GreetPM')
    try:
        autorole = ev.db.get_settings(server.id, 'AutoRole')
    except KeyError:
        ev.db.set_settings(server.id, 'AutoRole', None)
        autorole = None
    try:
        del_greet = ev.db.get_settings(server.id, 'GreetDelete')
    except:
        del_greet = False
    if greet:
        ev.db.add_stats('GreetCount')
        greet_message = ev.db.get_settings(server.id, 'GreetMessage')
        greet_message = greet_message.replace('%user_mention%', member.mention).replace('%server_name%',
                                                                                        server.name).replace(
            '%USER_MENTION%', member.mention).replace('%SERVER_NAME%', server.name.upper())
        if not greet_pm:
            greet_channel = ev.db.get_settings(server.id, 'GreetChannel')
            if not greet_channel:
                target_channel = server.default_channe
            else:
                target_channel = discord.utils.find(lambda x: x.id == greet_channel, member.guild.channels)
            greet_message_object = await target_channel.send(greet_message)
            if del_greet:
                await asyncio.sleep(10)
                await greet_message_object.delete()
        else:
            await member.send(greet_message)
    if autorole:
        target = None
        for role in member.guild.roles:
            if role.id == autorole:
                target = role
                break
        if target:
            await member.add_roles(target)
        else:
            await member.guild.default_channel.send(
                'I tried to assign the autorole to the user, but the AutoRole specified was not found so I reset the settings.')
            ev.db.set_settings(server.id, 'AutoRole', None)
