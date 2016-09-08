from plugin import Plugin
from config import cmd_nhentai
from config import cmd_rule34
from utils import create_logger
import sqlite3
import nhentai as nh


class NHentai(Plugin):
    is_global = True
    log = create_logger('nHentai')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_nhentai):
            await self.client.send_typing(message.channel)
            cmd_name = 'NHentai'
            dbsql = sqlite3.connect('storage/server_settings.sqlite', timeout=20)
            self.log.info('\nUser %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            try:
                perms = dbsql.execute("SELECT PERMITTED from NSFW where CHANNEL_ID=" + str(message.channel.id) + ";")
                permed = 'No'
                for row in perms:
                    permed = row[0]
            except sqlite3.OperationalError:
                permed = 'No'
            except SyntaxError:
                permed = 'No'
            if permed == 'Yes':
                permitted = True
            else:
                permitted = False
            # End Perms
            search = message.content[len(pfx) + len(cmd_rule34) + 1:]
            try:
                if search == '':
                    tags = 'nude'
                else:
                    pass
                n = 0
                list_text = '```'
                for entry in nh.search(search)['result']:
                    n += 1
                    list_text += '\n#' + str(n) + ' ' + entry['title']['pretty']
                if len(nh.search(search)['result']) > 1:
                    await self.client.send_message(message.channel, list_text + '\n```')
                    choice = await self.client.wait_for_message(author=message.author, channel=message.channel, timeout=20)
                    try:
                        nh_no = int(choice.content) - 1
                    except:
                        await self.client.send_message(message.channel,
                                                       'Not a number or timed out... Please start over')
                else:
                    nh_no = 0
                if nh_no > len(nh.search(search)['result']):
                    await self.client.send_message(message.channel, 'Number out of range...')
                else:
                    hen_name = nh.search(search)['result'][nh_no]['title']['pretty']
                    hen_id = nh.search(search)['result'][nh_no]['id']
                    hen_media_id = nh.search(search)['result'][nh_no]['media_id']
                    hen_url = ('https://nhentai.net/g/' + str(hen_id) + '/')
                    hen_img = ('https://i.nhentai.net/galleries/' + str(hen_media_id) + '/1.jpg')
                    nhen_text = ''
                    for tags in nh.search(search)['result'][nh_no]['tags']:
                        nhen_text += '[' + str(tags['name']).title() + '] '
                    if permitted is True:
                        await self.client.send_message(message.channel,'Name:\n```\n' + hen_name + '\n```\nTags:\n```\n' + nhen_text + '\n```\nImage: <' + hen_img + '>\nBook URL: <' + hen_url + '>')
                    else:
                        await self.client.send_message(message.channel,
                                                       'This channel does not have the NSFW Module permitted!')
            except SyntaxError:
                await self.client.send_message(message.channel, 'Nothing found...')
