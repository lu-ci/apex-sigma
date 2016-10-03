from plugin import Plugin
from utils import create_logger
from config import cmd_gelbooru
from lxml import html
import requests
import random
import sqlite3


class Gelbooru(Plugin):
    is_global = True
    log = create_logger('Gelbooru')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_gelbooru):
            await self.client.send_typing(message.channel)
            cmd_name = 'Gelbooru'
            dbsql = sqlite3.connect('storage/server_settings.sqlite', timeout=20)
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            try:
                perms = dbsql.execute("SELECT PERMITTED from NSFW where CHANNEL_ID=?;", (str(message.channel.id),))
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
            tags = message.content[len(pfx) + len(cmd_gelbooru) + 1:]
            try:
                if tags == '':
                    tags = 'nude'
                else:
                    pass
                gelbooru_url = 'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=' + tags.replace(' ', '+')
                data = requests.get(gelbooru_url)
                posts = html.fromstring(data.content)
                choice = random.choice(posts)

                if permitted is True:
                    await self.client.send_message(message.channel, choice.attrib['file_url'])
                else:
                    await self.client.send_message(message.channel,
                                                   'This channel does not have the NSFW Module permitted!')
            except:
                await self.client.send_message(message.channel, 'Nothing found...')
