async def listselfroles(cmd, message, args):
    try:
        check_data = {
            'ServerID': message.server.id
        }
        role_list = []
        exists = 0
        check_results = cmd.db.find('SelfRoles', check_data)
        for result in check_results:
            exists += 1
            if exists > 0:
                role_list.append(result['RoleName'])
        if exists == 0:
            await cmd.bot.send_message(message.channel, 'No self assignable roles exist on this server.')
            return
        else:
            await cmd.bot.send_message(message.channel, 'List of self assiglable roles for ' + message.server.name + ' is:\n```\n' + ', '.join(
                role_list) + '\n```')
    except SyntaxError as e:
        cmd.log.error(e)
        await cmd.bot.send_message(message.channel, 'An error was made.')
