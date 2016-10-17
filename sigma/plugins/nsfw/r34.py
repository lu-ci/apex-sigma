import requests
import random
from lxml import html

from sigma.plugin import Plugin
from sigma.utils import create_logger
from sigma.database import DatabaseError


class R34(Plugin):
    is_global = True
    log = create_logger('Rule34')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'rule34'):
            await self.client.send_typing(message.channel)
            cmd_name = 'Rule34'

            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)

            try:
                ch_id = str(message.channel.id)
                query = 'SELECT PERMITTED FROM NSFW WHERE CHANNEL_ID=?'
                perms = self.db.execute(query, ch_id)

                permed = 'No'
                for row in perms:
                    permed = row[0]
            except DatabaseError:
                permed = 'No'
            except:
                permed = 'No'

            if permed == 'Yes':
                permitted = True
            else:
                permitted = False

            tags = message.content[len(pfx) + len('rule34') + 1:]

            try:
                if tags == '':
                    tags = 'nude'
                else:
                    pass

                r34_url = 'http://rule34.xxx/index.php?page=dapi&s=post&q=index&tags=' + tags.replace(' ', '+')
                data = requests.get(r34_url)
                posts = html.fromstring(data.content)
                choice = random.choice(posts)

                if permitted is True:
                    await self.client.send_message(message.channel,
                                                   str(choice.attrib['file_url']).replace('//img', 'http://img'))
                else:
                    await self.client.send_message(message.channel,
                                                   'This channel does not have the NSFW Module permitted!')
            except:
                await self.client.send_message(message.channel, 'Nothing found...')
