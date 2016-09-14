from plugin import Plugin
from config import cmd_remind, donators
import asyncio
from utils import create_logger
from utils import bold\


class Reminder(Plugin):
    is_global = True
    log = create_logger(cmd_remind)

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_remind + ' '):
            await self.client.send_typing(message.channel)
            cmd_name = 'Reminder'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            remind_input = message.content[len(pfx) + len(cmd_remind) + 1:]
            try:
                time, ignore, remind_text = str(remind_input).partition(' ')
            except:
                remind_text = 'Nothing'
                time = '0'
                await self.client.send_message(message.channel,
                                               'Input missing parameters.\nThe command format is **' + pfx + cmd_remind + '[time in seconds] [message]**\nExample: ' + pfx + cmd_remind + ' 60 Leeroy jenkins!')
            try:
                if remind_text == '':
                    remind_text = 'Nothing'
                await self.client.send_message(message.channel, 'Okay! Reminder for\n[' + bold(
                    str(remind_text)) + ']\nis set and will be activated in `' + time + '` seconds! :clock:')
                await asyncio.sleep(int(time))
                await self.client.send_typing(message.channel)
                await self.client.send_message(message.channel,
                                               '<@' + message.author.id + '> Time\'s up! Let\'s do this! :clock: \n :exclamation: ' + bold(
                                                   str(remind_text)) + ' :exclamation: ')
            except:
                await self.client.send_message(message.channel,
                                               'Something went wrong with setting the timer, are you sure you inputed a number?')


class Donators(Plugin):
    is_global = True
    log = create_logger('Donators')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'donors'):
            await self.client.send_typing(message.channel)
            cmd_name = 'Reminder'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            out_text = ''
            for donor in donators:
                out_text += '\n' + bold(str(donor)) + ' :ribbon: '
            await self.client.send_message(message.channel, out_text)