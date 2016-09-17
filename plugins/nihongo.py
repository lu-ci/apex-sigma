from plugin import Plugin
from config import cmd_jisho
from config import cmd_wk
from config import cmd_wk_store
from utils import create_logger
import sqlite3
from utils import bold
import datetime
import requests
import json
from lxml import html


class WK(Plugin):
    is_global = True
    log = create_logger(cmd_wk)

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_wk):
            await self.client.send_typing(message.channel)
            cmd_name = 'WaniKani'
            dbsql = sqlite3.connect('storage/server_settings.sqlite', timeout=20)
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)

            if len(message.mentions) == 0:  # no mentions in the message
                if message.content == (pfx + cmd_wk):
                    user_id = str(message.author.id)  # if no arguments passed, pulling the ID of a caller
                else:
                    key = None
                    username = message.content[
                               len(pfx) + len(cmd_wk) + 1:]  # otherwise, pull the username out of a message
            else:  # if there are mentions in the message
                try:
                    user_id = message.mentions[0].id  # pull the mentioned ID
                except:
                    await self.client.send_message(message.channel, 'Error while parsing the input message')

            if 'username' not in locals():
                if 'user_id' not in locals():
                    await self.client.send_message(message.channel, 'No arguments passed')
                    return
                else:  # a username was passed
                    key_cur = dbsql.execute("SELECT WK_KEY, WK_USERNAME from WANIKANI where USER_ID=?;",
                                            (str(user_id),))
                    db_response = key_cur.fetchone()
                    if db_response == None:
                        await self.client.send_message(message.channel, 'No assigned key or username was found\n'
                                                                        'You can add it by sending me a direct message, for example\n'
                                                                        '`' + pfx + cmd_wk_store + ' key <your API key>` or `' + pfx + cmd_wk_store + ' username <your username>`')
                        return
                    print(db_response)
                    key = db_response[0]
                    username = db_response[1]
                    if (key == ''): key = None  # None the key if its empty so the if below won't be confused

            # pull data to parse from
            if key != None:  # if we have a key, pull data directly from API
                try:
                    url = 'https://www.wanikani.com/api/user/' + key
                    api = requests.get(url + '/srs-distribution').json()
                    api2 = requests.get(url + '/level-progression').json()
                    api3 = requests.get(url + '/study-queue').json()
                    rad = 'Radicals: Total: ' + bold(
                        str(api2['requested_information']['radicals_total'])) + ' | Done: ' + bold(
                        str(api2['requested_information']['radicals_progress']))
                    kanji = 'Kanji: Total: ' + bold(
                        str(api2['requested_information']['kanji_total'])) + ' | Done: ' + bold(
                        str(api2['requested_information']['kanji_progress']))

                    try:
                        next_review_date = bold(
                            datetime.datetime.fromtimestamp(api3['requested_information']['next_review_date']).strftime(
                                '%B %d, %Y %H:%M'))
                    except TypeError:
                        pass  # NoneType on retrival, user is on vacation
                    lesson_queue = bold(str(api3['requested_information']['lessons_available']))
                    review_queue = bold(str(api3['requested_information']['reviews_available']))
                    review_nh = bold(str(api3['requested_information']['reviews_available_next_hour']))
                    review_nd = bold(str(api3['requested_information']['reviews_available_next_day']))
                    if api3['requested_information']['reviews_available'] > 150:
                        warning = ':exclamation:'
                    else:
                        warning = ''
                except UnboundLocalError:
                    await self.client.send_message(message.channel,
                                                   'There doesn\'t seem to be a key tied to you...\n\nYou can add your key by sending a direct message to me with the the WKSave Command, for example:\n`' + pfx + cmd_wk_store + ' 16813135183151381`\nAnd just replace the numbers with your WK API Key!')
                    return
                except TypeError:
                    self.log.info('Type error')
                    return
            elif username != None:  # otherwise if we have a username, pull data from profile page
                page = requests.get('https://www.wanikani.com/community/people/' + username)
                tree = html.fromstring(page.content)
                try:
                    script = tree.xpath('//div[@class="footer-adjustment"]/script')[0].text.strip()
                except IndexError:
                    await self.client.send_message(message.channel,
                                                   "Error while parsing the page, profile not found or doesn't exist")
                    return
                script = script[script.find('var srsCounts'): script.find(
                    'Counts.fillInSrsCount(srsCounts.requested_information);')]
                script = script.strip()[16:-1]
                api = json.loads(script)
            else:
                await self.client.send_message(message.channel, 'No key or username')
                return

            # parsing
            try:
                out = ''

                username = api['user_information']['username']
                title = api['user_information']['title']
                level = str(api['user_information']['level'])
                creation_date = datetime.datetime.fromtimestamp(api['user_information']['creation_date']).strftime(
                    '%B %d, %Y')
                topics_count = str(api['user_information']['topics_count'])
                posts_count = str(api['user_information']['posts_count'])
                apprentice = 'Apprentice: ' + bold(str(api['requested_information']['apprentice']['total']))
                guru = 'Guru: ' + bold(str(api['requested_information']['guru']['total']))
                master = 'Master: ' + bold(str(api['requested_information']['master']['total']))
                enlightned = 'Enlightened: ' + bold(str(api['requested_information']['enlighten']['total']))
                burned = 'Burned: ' + bold(str(api['requested_information']['burned']['total']))

                out += bold(username) + ' of ' + bold('Sect ' + title) + '\n'
                out += bold('Level ' + level) + ' Apprentice' + '\n'
                out += 'Scribed ' + bold(topics_count + ' topics') + ' & ' + bold(posts_count + ' posts') + '\n'
                out += 'Serving the Crabigator since ' + bold(creation_date) + '\n'
                out += apprentice + ' | ' + guru + ' | ' + master + ' | ' + enlightned + ' | ' + burned + '\n'

                if 'api2' in locals():
                    out += rad + ' || ' + kanji + '\n'

                if 'api3' in locals():
                    try:
                        out += 'Your Next Review: ' + next_review_date + '\n'
                    except UnboundLocalError:
                        pass  # no review date, user is on vacation
                    out += 'Lesson Queue: ' + lesson_queue + ' | Review Queue: ' + review_queue + warning + '\n'
                    out += 'Reviews Next Hour: ' + review_nh + ' | Reviews Next Day: ' + review_nd
                await self.client.send_message(message.channel, out)
            except:
                self.log.info('Error while parsing the data')
                await self.client.send_message(message.channel,
                                               'Something went wrong ¯\_(ツ)_/¯. Error while parsing the data')
                return


class WKKey(Plugin):
    is_global = True
    log = create_logger(cmd_wk_store)

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_wk_store):
            try:
                await self.client.delete_message(message)
            except:
                print('Message in private channel, unable to delete...')
                pass
            try:
                await self.client.send_typing(message.channel)
            except:
                pass
            cmd_name = 'WaniKani Key Save'
            user_id = str(message.author.id)
            self.log.info('User %s [%s], used the ' + cmd_name + ' command.', message.author, user_id)

            try:
                args = message.content[len(pfx) + len(cmd_wk_store) + 1:]

                mode = args[:args.find(' ')].strip()
                payload = args[args.find(' ') + 1:].strip()  # key or username

                print(args)
                print(mode)
                print(payload)

                if mode == '':
                    await self.client.send_message(message.channel,
                                                   'Bind your Discord profile and your API key or username\n'
                                                   'Usage: `' + pfx + cmd_wk_store + ' key <your api key here>` or `' + pfx + cmd_wk_store + ' username <your username here>`')
                    return
                if mode not in ['key', 'username', 'remov']:  # remove
                    await self.client.send_message(message.channel, 'Unknown argument')
                    return
                if mode == 'key':
                    if len(payload) < 32 or len(payload) > 32:
                        await self.client.send_message(message.channel, 'The Key Seems Invalid...')
                        return

                dbsql = sqlite3.connect('storage/server_settings.sqlite', timeout=20)

                if mode == 'remov':  # remove
                    query = "DELETE from WANIKANI where USER_ID=?;"
                    dbsql.execute(query, (user_id,))
                    dbsql.commit()
                    await self.client.send_message(message.channel, 'Record deleted')
                    return

                try:
                    if mode == 'key': query = "INSERT INTO WANIKANI (USER_ID, WK_KEY) VALUES (?, ?)"
                    if mode == 'username': query = "INSERT INTO WANIKANI (USER_ID, WK_USERNAME) VALUES (?, ?)"
                    dbsql.execute(query, (user_id, payload))
                    dbsql.commit()
                    await self.client.send_message(message.channel, mode.capitalize() + ' Safely Stored. :key:')
                except sqlite3.IntegrityError:
                    await self.client.send_message(message.channel,
                                                   'A Key for your User ID already exists, removing...')
                    dbsql.execute("DELETE from WANIKANI where USER_ID=?;", (user_id,))
                    dbsql.execute(query, (user_id,))
                    dbsql.commit()
                    await self.client.send_message(message.channel,
                                                   'New ' + mode.capitalize() + ' Safely Stored. :key:')
                except UnboundLocalError:
                    await self.client.send_message(message.channel,
                                                   'There doesn\'t seem to be a key or username tied to you...\nYou can add your it by sending a direct message to me with the WKSave Command, for example:\n`' + pfx + cmd_wk_store + ' 16813135183151381`\nand just replace the numbers with your WK API Key!')
                except SyntaxError:
                    await self.client.send_message(message.channel, 'Something went horribly wrong!')

            except:
                await self.client.send_message(message.channel, 'Error while parsing the input message')


class Jisho(Plugin):
    is_global = True
    log = create_logger(cmd_jisho)

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_jisho):
            await self.client.send_typing(message.channel)
            cmd_name = 'Jisho'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            jisho_q = message.content[len(pfx) + len(cmd_jisho) + 1:]
            request = requests.get('http://jisho.org/api/v1/search/words?keyword=' + jisho_q).json()
            try:
                try:
                    is_common = '\"' + str(request['data'][0]['is_common']).title() + '\"'
                except:
                    is_common = '\"False\"'
                try:
                    ja_word = '\"' + request['data'][0]['japanese'][0]['word'] + '\"'
                except:
                    ja_word = '\"None\"'
                try:
                    ja_reading = '\"' + request['data'][0]['japanese'][0]['reading'] + '\"'
                except:
                    ja_reading = '\"None\"'
                try:
                    eng_def = ''
                    eng_def_data = request['data'][0]['senses'][0]['english_definitions']
                    for eng in eng_def_data:
                        eng_def += '\"' + str(eng) + '\", '
                except:
                    eng_def = '\"None\", '
                try:
                    info = '\"' + request['data'][0]['senses'][0]['info'][0] + '\"'
                except:
                    info = '\"None\"'
                try:
                    tags = ''
                    tags_data = request['data'][0]['tags']
                    for tag in tags_data:
                        tags += '\"' + str(tag) + '\", '
                except:
                    tags = '\"None\", '
                if tags == '':
                    tags = '\"None\", '
                try:
                    p_of_s = ''
                    pofs_data = request['data'][0]['senses'][0]['parts_of_speech']
                    for pof in pofs_data:
                        p_of_s += '\"' + str(pof) + '\", '
                except:
                    p_of_s = '\"None\", '
                if p_of_s == '':
                    p_of_s = '\"None\", '
                try:
                    s_tag = ''
                    s_tag_data = request['data'][0]['senses'][0]['tags']
                    for tag in s_tag_data:
                        s_tag += '\"' + str(tag) + '\", '
                except:
                    s_tag = '\"None\", '
                if s_tag == '':
                    s_tag = '\"None\", '
                result_text = ('Search query for `' + jisho_q + '`:\n```java' +
                               '\nJapanese Word: ' + ja_word +
                               '\nJapanese Reading: ' + ja_reading +
                               '\nEnglish Definition: ' + eng_def[:-2] +
                               '\nInfo: ' + info +
                               '\nCommon word: ' + is_common +
                               '\nParts of Speech: ' + p_of_s[:-2] +
                               '\nTags: ' + tags[:-2].replace('wanikani', 'WaniKani Level ') +
                               '\nSense Tags: ' + s_tag[:-2] +
                               '\n```')
                await self.client.send_message(message.channel, result_text)
            except:
                await self.client.send_message(message.channel, 'The word was not found or the API dun goofed.')
