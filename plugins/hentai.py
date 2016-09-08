from plugin import Plugin
from config import cmd_nhentai
from config import cmd_ehentai
from config import cmd_gelbooru
from config import cmd_rule34
from config import cmd_e621
from config import cmd_hentaims
from config import cmd_nsfw_permit
from utils import create_logger
from lxml import html
import requests
import random
import sqlite3


class NSFWPermission(Plugin):
    is_global = True
    log = create_logger(cmd_nsfw_permit)

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_nsfw_permit):
            await self.client.send_typing(message.channel)
            cmd_name = 'NSFW Permit'
            dbsql = sqlite3.connect('storage/server_settings.sqlite', timeout=20)
            sql_cmd_yes = ("INSERT INTO NSFW (CHANNEL_ID, PERMITTED) \
                                                  VALUES (chnl, 'perm')").replace('chnl', message.channel.id).replace(
                'perm',
                'Yes')
            sql_cmd_no = ("INSERT INTO NSFW (CHANNEL_ID, PERMITTED) \
                                                  VALUES (chnl, 'perm')").replace('chnl', message.channel.id).replace(
                'perm',
                'Yes')
            self.log.info('\nUser %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            admin_check = message.author.permissions_in(message.channel).administrator
            if admin_check is True:
                try:
                    dbsql.execute(sql_cmd_yes)
                    dbsql.commit()
                    await self.client.send_message(message.channel,
                                                   'The NSFW Module has been Enabled for <#' + message.channel.id + '>! :eggplant:')
                except sqlite3.IntegrityError:
                    dbsql.execute("DELETE from NSFW where CHANNEL_ID=" + message.channel.id + ";")
                    dbsql.commit()
                    await self.client.send_message(message.channel, 'Permission reverted to **Disabled**! :fire:')
            else:
                await self.client.send_message(message.channel,
                                               'Only an **Administrator** can manage permissions. :dark_sunglasses:')


class Hentai(Plugin):
    is_global = True
    log = create_logger('hentai')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_gelbooru):
            await self.client.send_typing(message.channel)
            cmd_name = 'GelBooru'
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

                if permitted == True:
                    await self.client.send_message(message.channel, choice.attrib['file_url'])
                else:
                    await self.client.send_message(message.channel,
                                                   'This channel does not have the NSFW Module permitted!')
            except:
                await self.client.send_message(message.channel, 'Nothing found...')
        elif message.content.startswith(pfx + cmd_nhentai + ' '):
            await self.client.send_typing(message.channel)
            cmd_name = 'NHentai'
            self.log.info('\nUser %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            # stuff
        elif message.content.startswith(pfx + cmd_ehentai + ' '):
            await self.client.send_typing(message.channel)
            cmd_name = 'EHentai'
            self.log.info('\nUser %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            # stuff
        elif message.content.startswith(pfx + cmd_e621 + ' '):
            await self.client.send_typing(message.channel)
            cmd_name = 'E621'
            self.log.info('\nUser %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            # stuff
        elif message.content.startswith(pfx + cmd_rule34 + ' '):
            await self.client.send_typing(message.channel)
            cmd_name = 'Rule34'
            self.log.info('\nUser %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            # stuff
        elif message.content.startswith(pfx + cmd_hentaims + ' '):
            await self.client.send_typing(message.channel)
            cmd_name = 'Hentai.MS'
            self.log.info('\nUser %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            # stuff
