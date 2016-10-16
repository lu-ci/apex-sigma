from plugin import Plugin
from config import donators, permitted_id
import asyncio
from utils import create_logger
from utils import bold
import time
from config import sigma_version
import aiohttp
import sys
import json


class Reminder(Plugin):
    is_global = True
    log = create_logger('remind')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'remind' + ' '):
            await self.client.send_typing(message.channel)
            cmd_name = 'Reminder'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            remind_input = message.content[len(pfx) + len('remind') + 1:]
            try:
                time_q, ignore, remind_text = str(remind_input).partition(' ')
            except:
                remind_text = 'Nothing'
                time_q = '0'
                await self.client.send_message(message.channel,
                                               'Input missing parameters.\nThe command format is **' + pfx + 'remind' + '[time in seconds] [message]**\nExample: ' + pfx + 'remind' + ' 60 Leeroy jenkins!')
            try:
                time_conv = time.strftime('%H:%M:%S', time.gmtime(int(time_q)))
                if remind_text == '':
                    remind_text = 'Nothing'
                confirm_msg = await self.client.send_message(message.channel, 'Okay! Reminder for\n[' + bold(
                    str(remind_text)) + ']\nis set and will be activated in `' + time_conv + '`! :clock:')
                time_num = int(time_q)
                while time_num > 0:
                    time_conv_second = time.strftime('%H:%M:%S', time.gmtime(int(time_num)))
                    await self.client.edit_message(confirm_msg, 'Okay! Reminder for\n[' + bold(
                        str(remind_text)) + ']\nis set and will be activated in `' + time_conv_second + '`! :clock:')
                    await asyncio.sleep(10)
                    time_num -= 10
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
            await self.client.send_message(message.channel,
                                           out_text + '\nPlease consider donating by hitting the Donate button on this page: <https://auroraproject.xyz/donors/>!')


class BulkMSG(Plugin):
    is_global = True
    log = create_logger('BulkMSG')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'bulkmsg'):
            await self.client.send_typing(message.channel)
            cmd_name = 'Bulk Message'
            # Start Logger
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            # Eng Logger
            input_message = message.content[len(pfx) + len('bulkmsg') + 1:]
            try:
                if message.author.id in permitted_id:
                    await self.client.send_message(message.channel,
                                                   'Starting bulk sending... Stand by for confirmation')
                    out = ''
                    printer = ''
                    no_s = 0
                    no_f = 0
                    for user in self.client.get_all_members():
                        if user.server.id == message.server.id and user.id != self.client.user.id:
                            try:
                                await self.client.start_private_message(user)
                                await self.client.send_message(user, input_message)
                                out += '\nSuccess: ' + user.name
                            except Exception as err:
                                out += '\nFailed: ' + user.name
                                printer += '\nFailed: ' + user.name + '\nReason: ' + str(err)
                                no_f += 1
                    await self.client.send_message(message.channel, 'Bulk message sending complete...\n' + out[:1900])
                    print(printer)
                    print('Succeeded: ' + str(no_s))
                    print('Failed: ' + str(no_f))
                else:
                    await self.client.send_message(message.channel,
                                                   'Not enough permissions, due to security issues, only a permitted user can use this for now...')
            except:
                print('Something went wrong. Most likely a basic error with the sending.')


class PMRedirect(Plugin):
    is_global = True
    log = create_logger('received pm')
    async def on_message(self, message, pfx):
        cid = self.client.user.id
        cmd_name = 'Private Message'
        if message.server is None:
            if str(message.author.id) == str(cid) or str(message.author.id) in permitted_id:
                return
            else:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
                for user in self.client.get_all_members():
                    if user.id in permitted_id:
                        private_msg_to_owner = await self.client.start_private_message(user=user)
                        await self.client.send_message(private_msg_to_owner,
                                                       '**' + message.author.name + '** (ID: ' + message.author.id + '):\n```' + message.content + '\n```')
                        return


class OtherUtils(Plugin):
    is_global = True
    log = create_logger('basic util')

    async def on_message(self, message, pfx):
        if message.content == (pfx + 'stats'):
            await self.client.send_typing(message.channel)
            cmd_name = 'Stats'
            # Start Logger
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)

            permed_ids = ', '.join(['[{:s}]'.format(x) for x in permitted_id])

            authors = ', '.join(['"{:s}"'.format(n) for n in self.client.authors])
            contributors = ', '.join(['"{:s}"'.format(n) for n in self.client.contributors])
            out_txt = '```python\n'
            out_txt += 'Logged In As: {:s}\n'.format(self.client.user.name)
            out_txt += 'User ID: {:s}\n'.format(self.client.user.id)
            out_txt += 'Authors: {:s}\n'.format(authors)
            out_txt += 'Contributors: {:s}\n'.format(contributors)
            out_txt += 'Sigma Version: {:s}\n'.format(sigma_version)
            out_txt += 'Connected to [ {:d} ] servers.\n'.format(self.client.server_count)
            out_txt += 'Serving [ {:d} ] users.\n'.format(self.client.member_count)
            out_txt += 'Permitted IDs: {:s}\n'.format(permed_ids)
            out_txt += '```'

            await self.client.send_message(message.channel, out_txt)
        elif message.content.startswith(pfx + 'setgame '):
            await self.client.send_typing(message.channel)
            cmd_name = 'Set Game'
            # Start Logger
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            if message.author.id in permitted_id:
                import discord
                gamename = message.content[len(pfx) + len('setgame') + 1:]
                game = discord.Game(name=gamename)
                await self.client.change_status(game)
                response = await self.client.send_message(message.channel, 'Done! :ok_hand:')
                await asyncio.sleep(5)
                await self.client.delete_message(response)
            else:
                response = await self.client.send_message(message.channel, 'Insufficient permissions...')
                await asyncio.sleep(5)
                await self.client.delete_message(response)
        elif message.content.startswith(pfx + 'servers'):
            await self.client.send_typing(message.channel)
            cmd_name = 'Servers'
            # Start Logger
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            if message.author.id in permitted_id:
                out_text = 'List of servers:\n```python'
                for server in self.client.servers:
                    out_text += '\n\"' + str(server) + '\" (' + str(server.id) + ')'
                if len(out_text) > 1950:
                    out_text = out_text[:1950]
                    out_text += '...'
                out_text += '\n```'
                await self.client.send_message(message.channel, out_text)
            else:
                error_msg = await self.client.send_message(message.channel, 'Insufficient permissions.')
                await asyncio.sleep(5)
                await self.client.delete_message(error_msg)
        elif message.content == pfx + 'kill':
            if message.author.id in permitted_id:
                sys.exit('terminated by command')


class SetAvatar(Plugin):
    is_global = True
    log = create_logger('Set Avatar')

    async def on_message(self, message, pfx, url=None, loop=None):
        if message.content.startswith(pfx + 'setavatar'):
            cmd_name = 'Set Avatar'
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            if message.author.id in permitted_id:
                loop = asyncio.get_event_loop() if loop is None else loop
                aiosession = aiohttp.ClientSession(loop=loop)
                try:
                    if message.attachments:
                        thing = message.attachments[0]['url']
                    else:
                        thing = url.strip('<>')
                    try:
                        with aiohttp.Timeout(10):
                            async with aiosession.get(thing) as res:
                                await self.client.edit_profile(avatar=await res.read())
                    except:
                        return
                except AttributeError:
                    try:
                        thing = message.content[len(pfx) + len('setavatar') + 1:]
                        try:
                            with aiohttp.Timeout(10):
                                async with aiosession.get(thing) as res:
                                    await self.client.edit_profile(avatar=await res.read())
                        except:
                            return
                    except ResourceWarning:
                        pass
                    except Exception as err:
                        await self.client.send_message(message.channel, str(err))


class MakeCommandList(Plugin):
    is_global = True
    log = create_logger('mkcmdlist')

    async def on_message(self, message, pfx):
        if message.content == pfx + 'mkcmdlist':
            cmd_name = 'Make Command List'
            await self.client.send_typing(message.channel)
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            if message.author.id in permitted_id:
                out_text = 'Command |  Description |  Usage'
                out_text += '\n--------|--------------|-------'
                try:
                    import os
                    os.remove('COMMANDLIST.md')
                except:
                    pass
                with open('storage/help.json', 'r', encoding='utf-8') as help_file:
                    help_data = help_file.read()
                    help_data = json.loads(help_data)
                for entry in help_data:
                    out_text += '\n`' + pfx + entry + '`  |  ' + help_data[entry]['description'].replace('%pfx%', str(
                        pfx)) + '  |  `' + help_data[entry]['usage'].replace('%pfx%', str(pfx)) + '`'
                with open("COMMANDLIST.md", "w") as text_file:
                    text_file.write(out_text)
                response = await self.client.send_message(message.channel, 'Done :ok_hand:')
                await asyncio.sleep(5)
                await self.client.delete_message(response)
            else:
                response = await self.client.send_message(message.channel, 'Unpermitted :x:')
                await asyncio.sleep(5)
                await self.client.delete_message(response)
