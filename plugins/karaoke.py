from plugin import Plugin
from utils import create_logger
from config import cmd_handup
from config import cmd_handdown
from config import cmd_takemic
from config import cmd_dropmic
import sys
from config import cmd_repertoire
import sqlite3


class Karaoke(Plugin):
    is_global = True
    log = create_logger(cmd_handup)

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_handup):
            try:
                await self.client.send_typing(message.channel)
                cmd_name = 'Raise Hand'
                dbsql = sqlite3.connect('storage/server_settings.sqlite', timeout=20)
                sql_cmd_yes = "INSERT INTO KARAOKE (SINGER_ID) VALUES (?)"
                self.log.info('\nUser %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
                try:
                    dbsql.execute(sql_cmd_yes, (message.author.id,))
                    dbsql.commit()
                    await self.client.send_message(message.channel,
                                                   '<@' + message.author.id + '> has joined the singers list!\nA round of applause please! :musical_note: :clap:')
                except:
                    await self.client.send_message(message.channel,
                                                   'I\'m sorry <@' + message.author.id + '>, but you\'re already on the list...')
            except:
                await self.client.send_message(message.channel, sys.exc_info()[0])
        elif message.content.startswith(pfx + cmd_handdown):
            cmd_name = 'Lower Hand'
            dbsql = sqlite3.connect('storage/server_settings.sqlite', timeout=20)
            self.log.info('\nUser %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            try:
                dbsql.execute("DELETE from KARAOKE where SINGER_ID=?;", (message.author.id,))
                dbsql.commit()
                await self.client.send_message(message.channel,
                                               'You have been removed from the list!\nWe\'re sorry to see you go, <@' + message.author.id + '>... :cry:')
            except:
                await self.client.send_message(message.channel, 'I can\'t find you on the list...')
        elif message.content.startswith(pfx + cmd_repertoire):
            await self.client.send_typing(message.channel)
            cmd_name = 'Repertiore'
            dbsql = sqlite3.connect('storage/server_settings.sqlite', timeout=20)
            self.log.info('\nUser %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            singer_list = ''
            n = 0
            dbsql.row_factory = lambda cursor, row: row[0]
            c = dbsql.cursor()
            ids = c.execute('SELECT SINGER_ID FROM KARAOKE').fetchall()
            try:
                for sng_id in reversed(ids):
                    n += 1
                    singer_list += '\n#' + str(n) + ': <@' + str(sng_id) + '>'
                await self.client.send_message(message.channel, singer_list)
            except:
                await self.client.send_message(message.channel, 'The list seems to be either empty, or broken...')
        elif message.content.startswith(pfx + 'karaoke'):
            await self.client.send_typing(message.channel)
            cmd_name = 'Karaoke Commands List'
            dbsql = sqlite3.connect('storage/server_settings.sqlite', timeout=20)
            self.log.info('\nUser %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            await self.client.send_message(message.channel,
                                           '```css\n[' + pfx + cmd_handup + '] Adds you to the singers list.' +
                                           '\n[' + pfx + cmd_handdown + '] Removes you to the singers list.' +
                                           '\n[' + pfx + cmd_repertoire + '] Lists the current singers.' +
                                           '\n[' + pfx + cmd_takemic + '] Mutes everyone except you so you can start.' +
                                           '\n[' + pfx + cmd_dropmic + '] Unmutes everyone and marks your performance as done.' +
                                           '\n[' + pfx + 'karaoke' + '] Lists these commands.' +
                                           '\n```')
