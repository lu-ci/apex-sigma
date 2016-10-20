class PMRedirect(Plugin):
    is_global = True
    log = create_logger('received pm')
    async def on_message(self, message, pfx):
        cid = self.client.user.id
        cmd_name = 'Private Message'
        if message.server is None:
            if str(message.author.id) == str(cid) or str(message.author.id) in permitted_id:
                return
            else:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
                for user in self.client.get_all_members():
                    if str(user.id) == str(permitted_id[0]):
                        private_msg_to_owner = await self.client.start_private_message(user=user)
                        await self.client.send_message(private_msg_to_owner,
                                                       '**' + message.author.name + '** (ID: ' + message.author.id + '):\n```' + message.content + '\n```')
                        return
