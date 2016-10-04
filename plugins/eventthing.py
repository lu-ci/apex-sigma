from plugin import Plugin
from utils import create_logger
from utils import getArguments
from utils import split_list
import sqlite3
from random import sample

class EventThing(Plugin):
    is_global = True
    cmd_ = 'Event'
    log = create_logger(cmd_)

    async def on_message(self, message, pre):
        if message.content.startswith(pre + 'eventsignup'):

            userid = message.author.id
            dbsql = sqlite3.connect('storage/server_settings.sqlite', timeout=5)

            query = "SELECT userid FROM EVENT WHERE userid=?;"
            result = dbsql.execute(query, (userid,)).fetchone()

            if result != None:
                await self.client.send_message(message.channel, 'Already signed up')
                return

            query = "INSERT INTO EVENT (userid) VALUES(?);"
            dbsql.execute(query, (userid,))
            dbsql.commit()
            #self.log.info('%s | %s [%s] on %s [%s] in #%s',
            #              cmd_, message.author, message.author.id, message.server.name, message.server.id, message.channel)

            await self.client.send_message(message.channel, 'Added')

        if message.content.startswith(pre + 'eventsignout'):

            userid = message.author.id
            dbsql = sqlite3.connect('storage/server_settings.sqlite', timeout=5)

            query = "SELECT userid FROM EVENT WHERE userid=?;"
            result = dbsql.execute(query, (userid,)).fetchone()

            if result == None:
                await self.client.send_message(message.channel, 'Already signed out')
                return

            query = "DELETE FROM EVENT WHERE userid=?;"
            dbsql.execute(query, (userid,))
            dbsql.commit()
            #self.log.info('%s | %s [%s] on %s [%s] in #%s',
            #              cmd_, message.author, message.author.id, message.server.name, message.server.id, message.channel)

            await self.client.send_message(message.channel, 'Removed')

        if message.content.startswith(pre + 'listparticipants'):

            dbsql = sqlite3.connect('storage/server_settings.sqlite', timeout=5)

            query = "SELECT userid FROM EVENT;"
            result = dbsql.execute(query).fetchall()

            if result == []:
                await self.client.send_message(message.channel, 'No participants')
                return

            out = 'Participants: \n'
            for row in result:
                participant = row[0]
                out += '<@#participant> \n'.replace('#participant', str(participant))

            #self.log.info('%s | %s [%s] on %s [%s] in #%s',
            #              cmd_, message.author, message.author.id, message.server.name, message.server.id, message.channel)

            await self.client.send_message(message.channel, out)

        if message.content.startswith(pre + 'teamgen'):
            teams = getArguments(message.content[len(pre) + len('teamgen'):], ' ')[0]
            dbsql = sqlite3.connect('storage/server_settings.sqlite', timeout=5)

            query = "SELECT userid FROM EVENT;"
            result = dbsql.execute(query).fetchall()

            if result == []:
                await self.client.send_message(message.channel, 'No participants')
                return

            participants = []
            for row in result: participants.append(row[0])

            #shuffle and split the list
            participants = sample(participants, len(participants))
            participants = split_list(participants, int(teams))

            out = ''
            for i in range(0, len(participants)):
                out += 'Team ' + str(i + 1) + '\n'
                for member in participants[i]:
                    out += '<@#member> \n'.replace('#member', str(member))
                out += '\n'

            print(participants)
                #out += '<@#participant> \n'.replace('#participant', str(participant))

            #self.log.info('%s | %s [%s] on %s [%s] in #%s',
            #              cmd_, message.author, message.author.id, message.server.name, message.server.id, message.channel)

            await self.client.send_message(message.channel, out)


