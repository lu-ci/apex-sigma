from plugin import Plugin
from config import cmd_rule34
from utils import create_logger
from lxml import html
import requests
import random
import sqlite3


class R34(Plugin):
    is_global = True
    log = create_logger('Rule34')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_rule34):
            await self.client.send_typing(message.channel)
            cmd_name = 'Rule34'
            dbsql = sqlite3.connect('storage/server_settings.sqlite', timeout=20)
            self.log.info('\nUser %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            try:
                perms = dbsql.execute("SELECT PERMITTED from NSFW where CHANNEL_ID=" + str(message.channel.id) + ";")
                permed = 'No'
                for row in perms:
                    permed = row[0]
            except sqlite3.OperationalError:
                permed = 'No'
            except SyntaxError:
                permed = 'No'
            if permed == 'Yes':
                permitted = True
            else:
                permitted = False
            tags = message.content[len(pfx) + len(cmd_rule34) + 1:]
            try:
                if tags == '':
                    tags = 'nude'
                else:
                    pass
                r34_url = 'http://rule34.xxx/index.php?page=dapi&s=post&q=index&tags=' + tags.replace(' ', '+')
                data = requests.get(r34_url)
                posts = html.fromstring(data.content)
                choice = random.choice(posts)
                if permitted == True:
                    await self.client.send_message(message.channel,
                                                   str(choice.attrib['file_url']).replace('//img', 'http://img'))
                else:
                    await self.client.send_message(message.channel,
                                                   'This channel does not have the NSFW Module permitted!')
            except:
                await self.client.send_message(message.channel, 'Nothing found...')
