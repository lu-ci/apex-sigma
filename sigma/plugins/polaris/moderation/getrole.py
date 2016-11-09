async def getrole(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    else:
        try:
            role_name = args[0].lower()
            while role_name.endswith(' '):
                role_name = role_name[:-1]
            while role_name.startswith(' '):
                role_name = role_name[1:]
            role_list = []

            db_exists_check = 'SELECT EXISTS (SELECT ROLE_NAME FROM SELF_ROLE WHERE SERVER_ID=?);'
            db_role_select_all = 'SELECT ROLE_NAME FROM SELF_ROLE WHERE SERVER_ID=?'
            exists = 0
            db_exists_data = cmd.db.execute(db_exists_check, message.server.id)
            for result in db_exists_data:
                exists = result[0]
            if exists == 0:
                await cmd.bot.send_message(message.channel, 'No self assignable roles exist on this server.')
                return
            else:
                db_role_select_data = cmd.db.execute(db_role_select_all, message.server.id)
                for result in db_role_select_data:
                    for entry in result:
                        role_list.append(entry.lower())
                if role_name in role_list:
                    role_on_server = False
                    out_role = None
                    for role in message.server.roles:
                        if role_name.lower() == role.name.lower():
                            role_on_server = True
                            out_role = role
                    if role_on_server:
                        try:
                            if out_role in message.author.roles:
                                await cmd.bot.remove_roles(message.author, out_role)
                                await cmd.bot.send_message(message.channel, 'The role **' + out_role.name + '** has been removed from you.')
                            else:
                                await cmd.bot.add_roles(message.author, out_role)
                                await cmd.bot.send_message(message.channel, 'You\'ve been assigned the **' + out_role.name + '** role.')
                        except Exception as e:
                            cmd.log.error(e)
                            await cmd.bot.send_message(message.channel, str(e))
                    else:
                        await cmd.bot.send_message(message.channel, 'The role was found in the database but not on the server.\nRemoving from DB...')
                        delete_query = "DELETE FROM SELF_ROLE WHERE SERVER_ID=? AND ROLE_NAME=?;"
                        cmd.db.execute(delete_query, message.server.id, role_name)
                        cmd.db.commit()
                else:
                    await cmd.bot.send_message(message.channel, 'The role was not found in the self assignable role list of this server.')
                    return
        except Exception as e:
            cmd.log.error(e)
            await cmd.bot.send_message(message.channel, 'An error was made.')
