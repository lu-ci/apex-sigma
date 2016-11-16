from sigma.core.permission import check_admin


async def blockinvites(cmd, message, args):
    if not check_admin(message.author, message.channel):
        await cmd.bot.send_message('Insufficient permissions. :x:')
        return
    else:
        active = False
        search_data = {
            'ServerID': message.server.id
        }
        activate_data = {
            'ServerID': message.server.id,
            'Active': True
        }
        activate_upd_data = {'$set': {
            'Active': True
        }}
        deactivate_upd_data = {'$set': {
            'Active': False
        }}
        n = 0
        exist_check = cmd.db.find('ServerFilterInvites', search_data)
        for result in exist_check:
            n += 1
            try:
                active = result['Active']
            except:
                pass
        if n == 0:
            cmd.db.insert_one('ServerFilterInvites', activate_data)
            await cmd.bot.send_message(message.channel, 'I **will** delete all messages containing a discord invite.')
        else:
            if active:
                cmd.db.update_one('ServerFilterInvites', {'ServerID': message.server.id}, deactivate_upd_data)
                await cmd.bot.send_message(message.channel, 'I **will not** delete any messages containing a discord invite.')
            else:
                cmd.db.update_one('ServerFilterInvites', {'ServerID': message.server.id}, activate_upd_data)
                await cmd.bot.send_message(message.channel, 'I **will** delete all messages containing a discord invite.')


