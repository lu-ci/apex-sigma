from sigma.plugin import Plugin
from sigma.utils import create_logger
from sigma.database import IntegrityError
import asyncio


class NSFWPermission(Plugin):
    is_global = True
    log = create_logger('nsfwpermit')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'nsfwpermit'):
            await self.client.send_typing(message.channel)
            cmd_name = 'NSFW Permit'

            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except Exception:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            admin_check = message.author.permissions_in(message.channel).administrator

            if admin_check is True:
                try:
                    query = "INSERT INTO NSFW (CHANNEL_ID, PERMITTED) VALUES (?, ?)"
                    self.db.execute(query, message.channel.id, 'Yes')
                    self.db.commit()
                    await self.client.send_message(message.channel,
                                                   'The NSFW Module has been Enabled for <#' + message.channel.id + '>! :eggplant:')
                except IntegrityError:
                    query = "DELETE from NSFW where CHANNEL_ID=?;"
                    self.db.execute(query, message.channel.id)
                    self.db.commit()
                    await self.client.send_message(message.channel, 'Permission reverted to **Disabled**! :fire:')
            else:
                response = await self.client.send_message(message.channel,
                                                          'Only an **Administrator** can manage permissions. :x:')
                await asyncio.sleep(10)
                await self.client.delete_message(response)
