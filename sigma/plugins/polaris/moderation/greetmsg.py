import asyncio


async def greetmsg(cmd, message, args):
    if message.server is not None:
        admin_check = message.author.permissions_in(message.channel).administrator
        if admin_check is True:
            msg_query = 'SELECT GREET_MSG FROM GREET WHERE SERVER_ID=?'
            chk_query = "SELECT EXISTS (SELECT SERVER_ID, GREET_CHANNEL_ID, ACTIVE, GREET_MSG FROM GREET WHERE SERVER_ID=?);"
            checker = cmd.db.execute(chk_query, message.server.id)
            existance = '0'
            for result in checker:
                existance = str(result[0])
            if existance == '0':
                await cmd.reply('No greet settings exist for this server.')
            else:
                if args:
                    greet_msg = ' '.join(args)
                    upd_msg_query = "UPDATE GREET SET GREET_MSG=? WHERE SERVER_ID=?"
                    cmd.db.execute(upd_msg_query, greet_msg, message.server.id)
                    cmd.db.commit()
                    await cmd.reply('**New Greet Message Set**')
                else:
                    greet_msg = ''
                    greet_grab = cmd.db.execute(msg_query, message.server.id)
                    for result in greet_grab:
                        greet_msg = result[0]
                    await cmd.reply('**Current greeting message is:**\n```\n' + greet_msg + '\n```')
    else:
        response = await cmd.reply('Only an **Administrator** can manage the greet message. :x:')
        await asyncio.sleep(10)
        await cmd.delete_message(response)
