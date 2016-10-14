from plugin import Plugin
from utils import create_logger
import sqlite3


class NSFWPermission(Plugin):
    is_global = True
    log = create_logger('nsfwpermit')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'nsfwpermit'):
            await self.client.send_typing(message.channel)
            cmd_name = 'NSFW Permit'
            dbsql = sqlite3.connect('storage/server_settings.sqlite', timeout=20)
            sql_cmd_yes = "INSERT INTO NSFW (CHANNEL_ID, PERMITTED) VALUES (?, ?)"
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
                try:
                    dbsql.execute(sql_cmd_yes, (message.channel.id, 'Yes'))
                    dbsql.commit()
                    await self.client.send_message(message.channel,
                                                   'The NSFW Module has been Enabled for <#' + message.channel.id + '>! :eggplant:')
                except sqlite3.IntegrityError:
                    dbsql.execute("DELETE from NSFW where CHANNEL_ID=?;", (message.channel.id,))
                    dbsql.commit()
                    await self.client.send_message(message.channel, 'Permission reverted to **Disabled**! :fire:')
            else:
                await self.client.send_message(message.channel,
                                               'Only an **Administrator** can manage permissions. :dark_sunglasses:')
