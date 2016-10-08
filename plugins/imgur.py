from plugin import Plugin
from utils import create_logger
from config import ImgurClientID, ImgurClientSecret
import random
import imgurpython

class Imgur(Plugin):
    is_global = True
    log = create_logger('imgur')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'imgur' + ' '):
            cmd_name = 'Imgur'
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            await self.client.send_typing(message.channel)
            q = message.content[len(pfx) + len('imgur') + 1:]
            imgur_client = imgurpython.ImgurClient(ImgurClientID, ImgurClientSecret)
            gallery_items = imgur_client.gallery_search(q, advanced=None, sort='time', window='all', page=0)
            try:
                chosen_item =random.choice(gallery_items).link
            except:
                await self.client.send_message(message.channel, 'No results...')
                return
            if chosen_item.startswith('http://i.imgur'):
                chosen_item = chosen_item
            else:
                chosen_item = chosen_item.replace('http://imgur', 'http://i.imgur').replace('/a/', '/') + '.png'
            await self.client.send_message(message.channel, chosen_item)
