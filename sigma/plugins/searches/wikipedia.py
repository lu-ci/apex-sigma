from sigma.utils import create_logger
from sigma.plugin import Plugin
import wikipedia


class Wikipedia(Plugin):
    is_global = True
    log = create_logger('wikipedia')

    async def on_message(self, message, pfx, ):
        if message.content.startswith(pfx + 'wiki' + ' '):
            await self.client.send_typing(message.channel)
            cmd_name = 'Wikipedia Search'
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            q = str(message.content[len(pfx) + len('wiki') + 1:]).lower()
            result = wikipedia.summary(q)
            await self.reply(result)
