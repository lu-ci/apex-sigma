import asyncio
import cleverbot

from sigma.plugin import Plugin
from sigma.utils import create_logger


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
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            try:
                clv_input = message.content[len(self.client.user.mention):]
                cb = cleverbot.Cleverbot()
                response = cb.ask(clv_input)
                await asyncio.sleep(len(response)*0.0145)
                await self.client.send_message(message.channel, '<@' + message.author.id + '> ' + response)
            except:
                await self.client.send_message(message.channel, 'Sorry <@' + message.author.id + '>, my brain isn\'t working at the moment give me some time to catch my breath...')
