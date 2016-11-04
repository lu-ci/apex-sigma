async def listselfroles(cmd, message, args):
    try:
        db_exists_check = 'SELECT EXISTS (SELECT ROLE_NAME FROM SELF_ROLE WHERE SERVER_ID=?);'
        db_role_select_all = 'SELECT ROLE_NAME FROM SELF_ROLE WHERE SERVER_ID=?'
        role_list = []
        exists = 0
        db_exists_data = cmd.db.execute(db_exists_check, message.server.id)
        for result in db_exists_data:
            exists = result[0]
        if exists == 0:
            await cmd.reply('No self assignable roles exist on this server.')
            return
        else:
            db_role_select_data = cmd.db.execute(db_role_select_all, message.server.id)
            for result in db_role_select_data:
                for entry in result:
                    role_list.append(entry.lower())
            await cmd.reply('List of self assiglable roles for ' + message.server.name + ' is:\n```\n' + ', '.join(
                role_list) + '\n```')
    except SyntaxError as e:
        cmd.log.error(e)
        await cmd.reply('An error was made.')
