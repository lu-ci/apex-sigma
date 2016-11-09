from sigma.core.permission import check_man_roles
from sigma.core.permission import check_admin

import asyncio
import random


async def role(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    else:
        try:
            if check_man_roles(message.author, message.channel):
                if len(args) < 2:
                    await cmd.bot.send_message(message.channel, cmd.help())
                    return
                else:
                    mode_list = ['create', 'destroy', 'give', 'take', 'auto', 'add', 'del']
                    mode = args[0].lower()
                    role_name = ' '.join(args[1:]).lower()
                    if message.mentions:
                        mention_text = ' <@' + message.mentions[0].id + '>'
                        role_name = role_name[:-(len(mention_text))]
                        if role_name.endswith(' '):
                            role_name = role_name[:-1]
                        if role_name.startswith(' '):
                            role_name = role_name[1:]
                    if mode not in mode_list:
                        await cmd.bot.send_message(message.channel, cmd.help())
                        return
                    else:
                        if mode == 'give' or mode == 'take':
                            if not message.mentions:
                                await cmd.bot.send_message(message.channel, cmd.help())
                                return
                            else:
                                target_usr = message.mentions[0]
                                if mode == 'give':
                                    role_choice = None
                                    for role_elem in message.server.roles:
                                        if role_elem.name.lower() == role_name.lower():
                                            role_choice = role_elem
                                    if role_choice is not None:
                                        try:
                                            await cmd.bot.add_roles(target_usr, role_choice)
                                        except Exception as e:
                                            cmd.log.error(e)
                                            await cmd.bot.send_message(message.channel, 'I can not edit the roles of that user.\n' + str(e))
                                            return
                                        await cmd.bot.send_message(message.channel, 
                                            'Role **' + role_name + '** has been given to ' + target_usr.name)
                                    else:
                                        await cmd.bot.send_message(message.channel, 'Role **' + role_name + '** has not been found.')
                                elif mode == 'take':
                                    role_choice = None
                                    for role_elem in message.server.roles:
                                        if role_elem.name.lower() == role_name.lower():
                                            role_choice = role_elem
                                    if role_choice is not None:
                                        try:
                                            await cmd.bot.remove_roles(target_usr, role_choice)
                                        except Exception as e:
                                            cmd.log.error(e)
                                            await cmd.bot.send_message(message.channel, 'I can not edit the roles of that user.\n' + str(e))
                                            return
                                        await cmd.bot.send_message(message.channel, 
                                            'Role **' + role_name + '** has been removed from ' + target_usr.name)
                                    else:
                                        await cmd.bot.send_message(message.channel, 'Role **' + role_name + '** has not been found.')
                        elif mode == 'create':
                            await cmd.bot.create_role(message.server, name=role_name)
                            await cmd.bot.send_message(message.channel, 'Role ' + role_name + ' has been created.')
                        elif mode == 'destroy':
                            role_choice = None
                            for role_elem in message.server.roles:
                                if role_elem.name.lower() == role_name.lower():
                                    role_choice = role_elem
                            if role_choice is not None:
                                await cmd.bot.delete_role(message.server, role_choice)
                                await cmd.bot.send_message(message.channel, 'Role **' + role_name + '** has been destroyed.')
                            else:
                                await cmd.bot.send_message(message.channel, 'Role **' + role_name + '** has not been found.')
                        elif mode == 'add':
                            role_on_server = False
                            for role_res in message.server.roles:
                                if role_name.lower() == role_res.name.lower():
                                    role_on_server = True
                                    break
                            if role_on_server:
                                role_check_results = cmd.db.find('SelfRoles', {'ServerID': message.server.id})
                                rol_exists_in_db = 0
                                self_role_data = {
                                    'ServerID': message.server.id,
                                    'RoleName': role_name
                                }
                                for result in role_check_results:
                                    rol_exists_in_db += 1
                                for result in role_check_results:
                                    rol_exists_in_db = result[0]
                                if rol_exists_in_db == 0:
                                    cmd.db.insert_one('SelfRoles', self_role_data)
                                    await cmd.bot.send_message(message.channel, 'Role **' + role_name + '** added to the self role database.')
                                else:
                                    role_search_data = {
                                        'ServerID': message.server.id,
                                        'RoleName': role_name
                                    }
                                    role_search = cmd.db.find('SelfRoles', role_search_data)
                                    res_count = 0
                                    for role in role_search:
                                        res_count += 1
                                    if res_count == 0:
                                        cmd.db.insert_one('SelfRoles', self_role_data)
                                        await cmd.bot.send_message(message.channel, 
                                            'Role **' + role_name + '** added to the self role database.')
                                    else:
                                        await cmd.bot.send_message(message.channel, 'This role is already in the database.')
                                        return
                        elif mode == 'del':
                            role_on_server = False
                            for role_res in message.server.roles:
                                if role_name.lower() == role_res.name.lower():
                                    role_on_server = True
                                    break
                            if role_on_server:
                                role_search_data = {
                                    'ServerID': message.server.id,
                                    'RoleName': role_name
                                }
                                role_search = cmd.db.find('SelfRoles', role_search_data)
                                res_count = 0
                                for role in role_search:
                                    res_count += 1
                                if res_count == 0:
                                    await cmd.bot.send_message(message.channel, 'This role is not in the database.')
                                else:
                                    cmd.db.delete_one('SelfRoles', role_search_data)
                                    await cmd.bot.send_message(message.channel, 'The role **' + role_name + '** has been removed from the database.')

                        elif mode == 'auto':
                            if check_admin:
                                role_on_server = False
                                for role_res in message.server.roles:
                                    if role_name.lower() == role_res.name.lower():
                                        role_on_server = True
                                        break
                                role_query = 'SELECT ROLE_NAME FROM AUTO_ROLE WHERE SERVER_ID=?'
                                chk_query = 'SELECT EXISTS (SELECT SERVER_ID, ROLE_NAME FROM AUTO_ROLE WHERE SERVER_ID=?);'
                                insert_query = 'INSERT INTO AUTO_ROLE (SERVER_ID, ROLE_NAME) VALUES (?, ?)'
                                update_query = 'UPDATE AUTO_ROLE SET ROLE_NAME=? WHERE SERVER_ID=?'
                                delete_query = "DELETE from AUTO_ROLE WHERE SERVER_ID=?;"
                                check_exist = cmd.db.execute(chk_query, message.server.id)
                                exists = None
                                for result in check_exist:
                                    exists = result[0]
                                if role_name.lower() == 'remove':
                                    if exists == 0:
                                        response = await cmd.bot.send_message(message.channel, 'There are no auto role settings to remove.')
                                        await asyncio.sleep(10)
                                        await cmd.bot.delete_message(response)
                                    else:
                                        cmd.db.execute(delete_query, message.server.id)
                                        cmd.db.commit()
                                        response = await cmd.bot.send_message(message.channel, 'The auto role has been removed.')
                                        await asyncio.sleep(10)
                                        await cmd.bot.delete_message(response)
                                elif role_name.lower() == 'remove' and exists == 0:
                                    response = await cmd.bot.send_message(message.channel, 'There are no auto role settings to remove.')
                                    await asyncio.sleep(10)
                                    await cmd.bot.delete_message(response)
                                else:
                                    if role_on_server == False:
                                        response = await cmd.bot.send_message(message.channel, 
                                            'The role ' + role_name + ' was not found on the server.')
                                        await asyncio.sleep(10)
                                        await cmd.bot.delete_message(response)
                                    else:
                                        if exists is not 0:
                                            role_name_check = cmd.db.execute(role_query, message.server.id)
                                            role_name_res = None
                                            for name in role_name_check:
                                                role_name_res = name[0]
                                            if role_name_res.lower() == role_name.lower():
                                                response = await cmd.bot.send_message(message.channel, 
                                                    'That role is the current Auto Role already.')
                                                await asyncio.sleep(10)
                                                await cmd.bot.delete_message(response)
                                            else:
                                                cmd.db.execute(update_query, role_name, message.server.id)
                                                cmd.db.commit()
                                                response = await cmd.bot.send_message(message.channel, 'The auto role has been updated.')
                                                await asyncio.sleep(10)
                                                await cmd.bot.delete_message(response)
                                        else:
                                            cmd.db.execute(insert_query, message.server.id, role_name)
                                            cmd.db.commit()
                                            response = await cmd.bot.send_message(message.channel, 
                                                'The auto role **' + role_name + '** has been set for ' + message.server.name + '.')
                                            await asyncio.sleep(10)
                                            await cmd.bot.delete_message(response)
                        else:
                            response = await cmd.bot.send_message(message.channel, 
                                'Only a user with **Administrator** privileges can use this function. :x:')
                            await asyncio.sleep(10)
                            await cmd.bot.delete_message(response)
            else:
                response = await cmd.bot.send_message(message.channel, 'Only a user with the **Manage Roles** privilege can use this command. :x:')
                await asyncio.sleep(10)
                await cmd.bot.delete_message(response)
        except SyntaxError as e:
            cmd.log.error(e)
            await cmd.bot.send_message(message.channel, 'We\'ve ran into an error.\n' + str(e))
