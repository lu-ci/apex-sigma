from sigma.plugin import Plugin
from sigma.utils import create_logger
import asyncio


class GreetingMessageToggle(Plugin):
    is_global = True
    log = create_logger('greet')

    async def on_message(self, message, pfx):
        if message.content == pfx + 'greet':
            if message.server is not None:
                default_greet_message = 'Hello %user_mention%, welcome to the %server_name%.'
                cmd_name = 'Greet Toggle'
                try:
                    self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                                  message.author,
                                  message.author.id, message.server.name, message.server.id, message.channel)
                except:
                    self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                                  message.author,
                                  message.author.id)
                admin_check = message.author.permissions_in(message.channel).administrator
                if admin_check is True:
                    init_query = "INSERT INTO GREET (SERVER_ID, GREET_CHANNEL_ID, ACTIVE, GREET_MSG) VALUES (?, ?, ?, ?)"
                    upd_act_query = "UPDATE GREET SET ACTIVE=? WHERE SERVER_ID=?"
                    upd_chn_query = "UPDATE GREET SET GREET_CHANNEL_ID=? WHERE SERVER_ID=?"
                    chk_query = "SELECT EXISTS (SELECT SERVER_ID, GREET_CHANNEL_ID, ACTIVE, GREET_MSG FROM GREET WHERE SERVER_ID=?);"
                    act_check = "SELECT ACTIVE FROM GREET WHERE SERVER_ID=?"
                    checker = self.db.execute(chk_query, message.server.id)

                    existance = '0'
                    for result in checker:
                        existance = str(result[0])
                    if existance == '0':
                        self.db.execute(init_query, message.server.id, message.channel.id, 'YES', default_greet_message)
                        self.db.commit()
                        await self.reply(
                            'Greet message activated for the server `' + message.server.name + '` on channel <#' + message.channel.id + '>.')
                    else:
                        chnl_check_query = "SELECT GREET_CHANNEL_ID FROM GREET WHERE SERVER_ID=?"
                        chnl_check = self.db.execute(chnl_check_query, message.server.id)
                        chnl_id = ''
                        for result in chnl_check:
                            chnl_id = result[0]
                        if str(chnl_id) == str(message.channel.id):
                            act_state = 'NO'
                            checker = self.db.execute(act_check, message.server.id)
                            for result in checker:
                                act_state = result[0]
                            if act_state == 'YES':
                                self.db.execute(upd_act_query, 'NO', message.server.id)
                                await self.reply('Greet message deactivated.')
                            elif act_state == 'NO':
                                self.db.execute(upd_act_query, 'YES', message.server.id)
                                await self.reply(
                                    'Greet message activated for the server `' + message.server.name + '` on channel <#' + message.channel.id + '>.')
                        else:
                            self.db.execute(upd_chn_query, message.channel.id, message.server.id)
                            self.db.execute(upd_act_query, 'YES', message.server.id)
                            await self.reply(
                                'Greet message activated for the server `' + message.server.name + '` on channel <#' + message.channel.id + '>.')
                        self.db.commit()
                else:
                    response = await self.client.send_message(message.channel,
                                                              'Only an **Administrator** can manage permissions. :x:')
                    await asyncio.sleep(10)
                    await self.client.delete_message(response)
        elif message.content == pfx + 'greetmsg':
            if message.server is not None:
                cmd_name = 'Greet Message Check'
                try:
                    self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                                  message.author,
                                  message.author.id, message.server.name, message.server.id, message.channel)
                except:
                    self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                                  message.author,
                                  message.author.id)
                admin_check = message.author.permissions_in(message.channel).administrator
                if admin_check is True:
                    msg_query = 'SELECT GREET_MSG FROM GREET WHERE SERVER_ID=?'
                    chk_query = "SELECT EXISTS (SELECT SERVER_ID, GREET_CHANNEL_ID, ACTIVE, GREET_MSG FROM GREET WHERE SERVER_ID=?);"
                    checker = self.db.execute(chk_query, message.server.id)
                    existance = '0'
                    for result in checker:
                        existance = str(result[0])
                    if existance == '0':
                        await self.reply('No greet settings exist for this server.')
                    else:
                        greet_msg = ''
                        greet_grab = self.db.execute(msg_query, message.server.id)
                        for result in greet_grab:
                            greet_msg = result[0]
                        await self.reply('**Current greeting message is:**\n' + greet_msg)
                else:
                    response = await self.client.send_message(message.channel,
                                                              'Only an **Administrator** can manage permissions. :x:')
                    await asyncio.sleep(10)
                    await self.client.delete_message(response)

