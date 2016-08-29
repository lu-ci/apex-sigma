from plugin import Plugin
from utils import create_logger
from config import OwnerID

class Jacob_Noah(Plugin):
    is_global = True
    log = create_logger('noah_stuff')

    async def on_message(self, message, pfx):
        if message.content.startswith('<@' + self.client.user.id + '> kish meh'):
            await self.client.send_typing(message.channel)
            cmd_name = 'Jacob Noah Meme'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            if message.author.id == OwnerID:
                await self.client.send_message(message.channel, 'Of course <@' + OwnerID + '>, my love, anything for you! Chu~')
            elif message.author.id == '113106144444030976':
                await self.client.send_message(message.channel, 'You don\'t need me <@' + message.author.id + '>, you have a lovely Canadian girl waiting for that large rod of yours~')
            elif message.author.id == '152239976338161664':
                await self.client.send_message(message.channel, 'Nuuuu~... <@' + message.author.id + '>, go ask Bubu!')
            else:
                await self.client.send_message(message.channel, 'Ew <@' + OwnerID + '>... Would kindly piss off...')