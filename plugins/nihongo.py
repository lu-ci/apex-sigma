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
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os
from io import BytesIO


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
                    rad_total = api2['requested_information']['radicals_total']
                    rad_curr = api2['requested_information']['radicals_progress']
                    kanji_total = api2['requested_information']['kanji_total']
                    kanji_curr = api2['requested_information']['kanji_progress']

                    try:
                        next_review_date = datetime.datetime.fromtimestamp(
                            api3['requested_information']['next_review_date']).strftime(
                            '%B %d, %Y %H:%M')
                    except TypeError:
                        pass  # NoneType on retrival, user is on vacation
                    lesson_queue = str(api3['requested_information']['lessons_available'])
                    review_queue = str(api3['requested_information']['reviews_available'])
                    review_nh = str(api3['requested_information']['reviews_available_next_hour'])
                    review_nd = str(api3['requested_information']['reviews_available_next_day'])
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
                img_type = 'Small'
                out = ''

                username = api['user_information']['username']
                title = api['user_information']['title']
                avatar = 'https://www.gravatar.com/avatar/' + api['user_information']['gravatar']
                level = api['user_information']['level']
                creation_date = datetime.datetime.fromtimestamp(api['user_information']['creation_date']).strftime(
                    '%B %d, %Y')
                topics_count = api['user_information']['topics_count']
                posts_count = api['user_information']['posts_count']
                apprentice = api['requested_information']['apprentice']['total']
                guru = api['requested_information']['guru']['total']
                master = api['requested_information']['master']['total']
                enlightned = api['requested_information']['enlighten']['total']
                burned = api['requested_information']['burned']['total']

                out += '\"' + username + '\"' + ' of ' + 'Sect \"' + title + '\"\n'
                out += 'Level \"' + str(level) + '\" Apprentice' + '\n'
                out += 'Scribed \"' + str(topics_count) + '\" topics' + ' & \"' + str(posts_count) + '\" posts' + '\n'
                out += 'Serving the Crabigator since \"' + creation_date + '\"\n'
                out += 'Apprentice: \"' + str(apprentice) + '\" | Guru: \"' + str(guru) + '\" | Master: \"' + str(
                    master) + '\" | Enlightened: \"' + str(
                    enlightned) + '\" | Burned: \"' + str(burned) + '\"\n'

                if 'api2' in locals():
                    img_type = 'Big'
                    out += 'Radicals: \"' + str(rad_curr) + '/' + str(rad_total) + '\" || Kanji: \"' + str(
                        kanji_curr) + '/' + str(
                        kanji_total) + '\"\n'

                if 'api3' in locals():
                    img_type = 'Big'
                    try:
                        out += 'Your Next Review: \"' + next_review_date + '\"\n'
                    except UnboundLocalError:
                        pass  # no review date, user is on vacation
                    out += 'Lesson Queue: \"' + lesson_queue + '\" | Review Queue: \"' + review_queue + warning + '\"\n'
                    out += 'Reviews Next Hour: \"' + review_nh + '\" | Reviews Next Day: \"' + review_nd + '\"'
                ava_raw = requests.get(avatar).content
                ava = Image.open(BytesIO(ava_raw))
                txt_color = (0, 125, 107)
                rank_category = ''
                kanji_loc = 174
                ov_color = ''
                if level <= 10:
                    rank_category = '快'
                    kanji_loc = 184
                    ov_color = '_pl'
                    txt_color = (204, 51, 255)
                elif 11 <= level <= 20:
                    kanji_loc = 184
                    rank_category = '苦'
                    ov_color = '_pai'
                    txt_color = (153, 102, 255)
                elif 21 <= level <= 30:
                    rank_category = '死'
                    kanji_loc = 184
                    ov_color = '_de'
                    txt_color = (102, 102, 255)
                elif 31 <= level <= 40:
                    rank_category = '地獄'
                    ov_color = '_he'
                    txt_color = (51, 102, 255)
                elif 41 <= level <= 50:
                    rank_category = '天堂'
                    ov_color = '_par'
                    txt_color = (0, 102, 255)
                elif 51 <= level <= 59:
                    rank_category = '現実'
                    ov_color = '_re'
                    txt_color = (0, 153, 255)
                elif level == 60:
                    rank_category = '発明'
                    ov_color = '_en'
                    txt_color = (0, 204, 255)
                base = Image.open('img/ani/base_wk_small.png')
                overlay = Image.open('img/ani/overlay_wk_small' + ov_color + '.png')
                if img_type == 'Small':
                    base = Image.open('img/ani/base_wk_small.png')
                    overlay = Image.open('img/ani/overlay_wk_small' + ov_color + '.png')
                elif img_type == 'Big':
                    base = Image.open('img/ani/base_wk.png')
                    overlay = Image.open('img/ani/overlay_wk' + ov_color + '.png')
                base.paste(ava, (15, 5))
                base.paste(overlay, (0, 0), overlay)
                review_color = (255, 255, 255)
                font1 = ImageFont.truetype("big_noodle_titling_oblique.ttf", 25)
                font2 = ImageFont.truetype("big_noodle_titling_oblique.ttf", 21)
                font3 = ImageFont.truetype("YuGothB.ttc", 21)
                font4 = ImageFont.truetype("big_noodle_titling_oblique.ttf", 20)
                review_font = font2
                review_pos = (420, 110)
                imgdraw = ImageDraw.Draw(base)
                imgdraw.text((95, 2), username + ' of sect ' + title, txt_color, font=font1)
                imgdraw.text((116, 31), str(apprentice), txt_color, font=font2)
                imgdraw.text((182, 31), str(guru), txt_color, font=font2)
                imgdraw.text((248, 31), str(master), txt_color, font=font2)
                imgdraw.text((314, 31), str(enlightned), txt_color, font=font2)
                imgdraw.text((380, 31), str(burned), txt_color, font=font2)
                imgdraw.text((95, 60), 'Level: ' + str(level), txt_color, font=font2)
                imgdraw.text((250, 60), 'Joined: ' + str(creation_date), txt_color, font=font2)
                imgdraw.text((kanji_loc, 61), rank_category, (255, 255, 255), font=font3)
                if img_type == 'Big':
                    try:
                        imgdraw.text((11, 88), 'Next Review: ' + str(next_review_date), (255, 255, 255), font=font2)
                    except:
                        imgdraw.text((11, 88), 'Next Review: ' 'On Vacation or No Data', (255, 255, 255), font=font2)
                    if int(review_queue) > 150:
                        review_color = (255, 174, 35)
                        review_font = font1
                        review_pos = (420, 108)
                    imgdraw.text((11, 110), 'Next Hour: ' + str(review_nh), (255, 255, 255), font=font4)
                    imgdraw.text((136, 110), 'Next Day: ' + str(review_nd), (255, 255, 255), font=font4)
                    imgdraw.text((252, 88), 'Radical: ' + str(rad_curr) + '/' + str(rad_total), (255, 255, 255),
                                 font=font2)
                    imgdraw.text((363, 88), 'Kanji: ' + str(kanji_curr) + '/' + str(kanji_total), (255, 255, 255),
                                 font=font2)
                    imgdraw.text((252, 110), 'Lessons: ' + str(lesson_queue), (255, 255, 255), font=font2)
                    imgdraw.text((363, 110), 'Reviews: ', (255, 255, 255), font=font2)
                    imgdraw.text(review_pos, str(review_queue), review_color, font=review_font)
                if img_type == 'Big':
                    try:
                        imgdraw.text((11, 88), 'Next Review: ' + str(next_review_date), (255, 255, 255), font=font2)
                    except:
                        imgdraw.text((11, 88), 'Next Review: ' 'On Vacation or No Data', (255, 255, 255), font=font2)
                    if int(review_queue) > 150:
                        review_color = (255, 174, 35)
                        review_font = font1
                        review_pos = (420, 108)
                    imgdraw.text((11, 110), 'Next Hour: ' + str(review_nh), (255, 255, 255), font=font4)
                    imgdraw.text((136, 110), 'Next Day: ' + str(review_nd), (255, 255, 255), font=font4)
                    imgdraw.text((252, 88), 'Radical: ' + str(rad_curr) + '/' + str(rad_total), (255, 255, 255),
                                 font=font2)
                    imgdraw.text((363, 88), 'Kanji: ' + str(kanji_curr) + '/' + str(kanji_total), (255, 255, 255),
                                 font=font2)
                    imgdraw.text((252, 110), 'Lessons: ' + str(lesson_queue), (255, 255, 255), font=font2)
                    imgdraw.text((363, 110), 'Reviews: ', (255, 255, 255), font=font2)
                    imgdraw.text(review_pos, str(review_queue), review_color, font=review_font)
                base.save('cache\\ani\\wk_' + message.author.id + '.png')
                await self.client.send_file(message.channel, 'cache\\ani\\wk_' + message.author.id + '.png')
                await self.client.send_message(message.channel, '```java\n' + out + '\n```')
                os.remove('cache\\ani\\wk_' + message.author.id + '.png')
            except SyntaxError:
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
