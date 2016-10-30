from sigma.core.permission import check_man_roles
import asyncio


async def role(cmd, message, args):
    if not args:
        await cmd.reply(cmd.help())
        return
    else:
        if check_man_roles:
            if len(args) < 2:
                await cmd.reply(cmd.help())
                return
            else:
                mode_list = ['create', 'destroy', 'give', 'take', 'auto', 'add', 'del']
                mode = args[0].lower()
                role_name = args[1]
                if mode not in mode_list:
                    await cmd.reply(cmd.help())
                    return
                else:
                    if mode == 'give' or mode == 'take':
                        if not message.mentions:
                            await cmd.reply(cmd.help())
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
                                        await cmd.reply('I can not edit the roles of that user.\n' + str(e))
                                        return
                                    await cmd.reply('Role ' + role_name + ' has been given to ' + target_usr.name)
                                else:
                                    await cmd.reply('Role ' + role_name + ' has not been found.')
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
                                        await cmd.reply('I can not edit the roles of that user.\n' + str(e))
                                        return
                                    await cmd.reply('Role ' + role_name + ' has been removed from ' + target_usr.name)
                                else:
                                    await cmd.reply('Role ' + role_name + ' has not been found.')
                    elif mode == 'create':
                        await cmd.bot.create_role(message.server, name=role_name)
                        await cmd.reply('Role ' + role_name + ' has been created.')
                    elif mode == 'destroy':
                        role_choice = None
                        for role_elem in message.server.roles:
                            if role_elem.name.lower() == role_name.lower():
                                role_choice = role_elem
                        if role_choice is not None:
                            await cmd.bot.delete_role(message.server, role_choice)
                            await cmd.reply('Role ' + role_name + ' has been destroyed.')
                        else:
                            await cmd.reply('Role ' + role_name + ' has not been found.')

        else:
            response = await cmd.reply('Only a user with the **Manage Roles** privilege can use this command. :x:')
            await asyncio.sleep(10)
            await cmd.bot.delete_message(response)
