from plugin import Plugin
from config import cmd_ehentai
from utils import create_logger

class EHentai(Plugin):
    is_global = True
    log = create_logger('eHentai')
    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_ehentai):
            await self.client.send_typing(message.channel)
            cmd_name = 'EHentai'
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)