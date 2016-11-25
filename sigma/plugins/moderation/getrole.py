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

            exists = 0
            db_exists_data = cmd.db.find('SelfRoles', {'ServerID': message.server.id})
            for result in db_exists_data:
                exists += 1
            if exists == 0:
                await cmd.bot.send_message(message.channel, 'No self assignable roles exist on this server.')
                return
            else:
                db_role_select_data = cmd.db.find('SelfRoles', {'ServerID': message.server.id})
                for result in db_role_select_data:
                    role_list.append(result['RoleName'])
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
                        cmd.db.delete_one('SelfRoles', {'ServerID': message.server.id, 'RoleName': role_name})
                else:
                    await cmd.bot.send_message(message.channel, 'The role was not found in the self assignable role list of this server.')
                    return
        except Exception as e:
            cmd.log.error(e)
            await cmd.bot.send_message(message.channel, 'An error was made.')
