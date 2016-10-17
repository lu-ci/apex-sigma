from plugin import Plugin
from utils import create_logger
from config import OwnerID as ownr
class Echo(Plugin):
    is_global = True
    log = create_logger('echo')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'echo' + ' '):
            cmd_name = 'Echo'
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            if message.author.id == ownr:
                await self.client.send_message(message.channel, message.content[len('echo') + len(pfx):])
            else:
                await self.client.send_message(message.channel,
                                    'Sorry, <@' + message.author.id + '>, you do not have permission to do that...')