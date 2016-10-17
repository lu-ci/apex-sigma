import asyncio
import json

from sigma.plugin import Plugin
from sigma.utils import create_logger, bold


class Help(Plugin):
    is_global = True
    log = create_logger('help')

    async def on_message(self, message, pfx):
        if message.content == (pfx + 'help'):
            cmd_name = 'Module List'
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            await self.client.send_typing(message.channel)
            help_msg = await self.client.send_message(message.channel, '```java' +
                                                      '\nHelp is being reworked...'
                                                      '\nExcuse us...'
                                                      '\n```' +
                                                      '\nMade by `Alex` with **love**!\n<https://github.com/AXAz0r/apex-sigma>')
            await asyncio.sleep(60)
            try:
                await self.client.delete_message(help_msg)
            except:
                print('Help Message Deletion Failed - Not found or something...')
                pass
        elif message.content.startswith(pfx + 'help '):
            cmd_name = 'Command Help'
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            await self.client.send_typing(message.channel)
            help_q = str(message.content[len(pfx) + len('help') + 1:])
            q = help_q.lower().replace(pfx, '')
            try:
                with open('storage/help.json', 'r', encoding='utf-8') as help_file:
                    help_data = help_file.read()
                    help_data = json.loads(help_data)
            except FileNotFoundError as err:
                print(err)
                return
            except Exception as err:
                print(err)
                return
            try:
                description = help_data[q]['description'].replace('%pfx%', str(pfx))
                usage = help_data[q]['usage'].replace('%pfx%', str(pfx))
            except KeyError as err:
                print(err)
                try:
                    await self.client.send_message(message.channel, 'Command Not Found')
                except:
                    pass
                return
            except Exception as err:
                try:
                    await self.client.send_message(message.channel, 'Error: ' + str(err))
                except:
                    pass
                return
            out_text = (
            bold('Description:') + '\n```\n' + description + '\n```\n' + bold('Usage: ') + '`' + usage + '`')
            await self.client.send_message(message.channel, out_text)
