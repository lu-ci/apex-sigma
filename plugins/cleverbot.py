from plugin import Plugin
from utils import create_logger
import cleverbot

class Cleverbot(Plugin):
    is_global = True
    log = create_logger('cleverbot')

    async def on_message(self, message, pfx):
        if message.content.startswith(self.client.user.mention):
            await self.client.send_typing(message.channel)
            cmd_name = 'Kiss Me'
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except AttributeError:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.channel)
            clv_input = message.content[len(self.client.user.mention):]
            cb = cleverbot.Cleverbot()
            response = cb.ask(clv_input)
            await self.client.send_message(message.channel, '<@' + message.author.id + '>' + response)