from plugin import Plugin
from config import cmd_hentaims
from utils import create_logger


class HentaiMS(Plugin):
    is_global = True
    log = create_logger('Hentai.MS')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_hentaims):
            await self.client.send_typing(message.channel)
            cmd_name = 'Hentai.MS'
            self.log.info('\nUser %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
