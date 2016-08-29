from plugin import Plugin
from config import cmd_nhentai
from config import cmd_ehentai
from config import cmd_gelbooru
from config import cmd_rule34
from config import cmd_e621
from config import cmd_hentaims
from utils import create_logger
import requests
import xml.etree.ElementTree
from random import randint

class Hentai(Plugin):
    is_global = True
    log = create_logger('hentai')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_gelbooru):
            await self.client.send_typing(message.channel)
            cmd_name = 'GelBooru'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            tags = message.content[len(pfx) + len(cmd_gelbooru) + 1:]
            if tags == '':
                tags = 'nude'
            else:
                pass
            print(tags)
            gelbooru_url = 'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=' + tags
            print(gelbooru_url)
            e = xml.etree.ElementTree.parse(gelbooru_url).getroot()
            print(e)
            rand_no = randint(0, 50)
            #document = requests.get(gelbooru_url)

        elif message.content.startswith(pfx + cmd_nhentai + ' '):
            await self.client.send_typing(message.channel)
            cmd_name = 'NHentai'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            #stuff
        elif message.content.startswith(pfx + cmd_ehentai + ' '):
            await self.client.send_typing(message.channel)
            cmd_name = 'EHentai'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            #stuff
        elif message.content.startswith(pfx + cmd_e621 + ' '):
            await self.client.send_typing(message.channel)
            cmd_name = 'E621'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            #stuff
        elif message.content.startswith(pfx + cmd_rule34 + ' '):
            await self.client.send_typing(message.channel)
            cmd_name = 'Rule34'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            #stuff
        elif message.content.startswith(pfx + cmd_hentaims + ' '):
            await self.client.send_typing(message.channel)
            cmd_name = 'Hentai.MS'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            #stuff