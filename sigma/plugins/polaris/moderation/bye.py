import asyncio

async def bye(cmd, message, args):
        if message.server is not None:
            default_bye_message = 'User %user_mention% has left %server_name%.'
            admin_check = message.author.permissions_in(message.channel).administrator
            if admin_check is True:
                init_query = "INSERT INTO BYE (SERVER_ID, BYE_CHANNEL_ID, ACTIVE, BYE_MSG) VALUES (?, ?, ?, ?)"
                upd_act_query = "UPDATE BYE SET ACTIVE=? WHERE SERVER_ID=?"
                upd_chn_query = "UPDATE BYE SET BYE_CHANNEL_ID=? WHERE SERVER_ID=?"
                chk_query = "SELECT EXISTS (SELECT SERVER_ID, BYE_CHANNEL_ID, ACTIVE, BYE_MSG FROM BYE WHERE SERVER_ID=?);"
                act_check = "SELECT ACTIVE FROM BYE WHERE SERVER_ID=?"
                checker = cmd.db.execute(chk_query, message.server.id)

                existance = '0'
                for result in checker:
                    existance = str(result[0])
                if existance == '0':
                    cmd.db.execute(init_query, message.server.id, message.channel.id, 'YES', default_bye_message)
                    cmd.db.commit()
                    await cmd.reply(
                        'Bye message activated for the server `' + message.server.name + '` on channel <#' + message.channel.id + '>.')
                else:
                    chnl_check_query = "SELECT BYE_CHANNEL_ID FROM BYE WHERE SERVER_ID=?"
                    chnl_check = cmd.db.execute(chnl_check_query, message.server.id)
                    chnl_id = ''
                    for result in chnl_check:
                        chnl_id = result[0]
                    if str(chnl_id) == str(message.channel.id):
                        act_state = 'NO'
                        checker = cmd.db.execute(act_check, message.server.id)
                        for result in checker:
                            act_state = result[0]
                        if act_state == 'YES':
                            cmd.db.execute(upd_act_query, 'NO', message.server.id)
                            await cmd.reply('Bye message deactivated.')
                        elif act_state == 'NO':
                            cmd.db.execute(upd_act_query, 'YES', message.server.id)
                            await cmd.reply(
                                'Bye message activated for the server `' + message.server.name + '` on channel <#' + message.channel.id + '>.')
                    else:
                        cmd.db.execute(upd_chn_query, message.channel.id, message.server.id)
                        cmd.db.execute(upd_act_query, 'YES', message.server.id)
                        await cmd.reply(
                            'Bye message activated for the server `' + message.server.name + '` on channel <#' + message.channel.id + '>.')
                        cmd.db.commit()
            else:
                response = await cmd.client.send_message(message.channel,
                                                          'Only an **Administrator** can manage permissions. :x:')
                await asyncio.sleep(10)
                await cmd.delete_message(response)
