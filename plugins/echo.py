from plugin import Plugin
from utils import create_logger
from config import cmd_echo
from config import Prefix as pfx
from config import OwnerID as ownr

class Echo(Plugin):
    is_global = True
    log = create_logger(cmd_echo)

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_echo + ' '):
            cmd_name = 'Echo'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            if message.author.id == ownr:
                await self.client.send_message(message.channel, message.content[len(cmd_echo) + len(pfx):])
            else:
                await self.client.send_message(message.channel,
                                    '<@' + message.author.id + '>, you do not have permission to do that...')