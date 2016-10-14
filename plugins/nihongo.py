from plugin import Plugin
from utils import create_logger
import datetime
import requests
import json
from lxml import html
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os
from io import BytesIO
from database import IntegrityError


class WK(Plugin):
    is_global = True
    log = create_logger('wanikani')

    img_base = 'img/ani'
    wk_base_url = 'https://www.wanikani.com/api/user/'

    def parse_date(self, time, fmt='%B %d, %Y %H:%M'):
        if time:
            return datetime.datetime.fromtimestamp(time).strftime(fmt)
        else:
            return 'Unknown'

    def get_rank_info(self, level, location=174):
        if level == 60:
            return ('発明', location, '_en', (0, 204, 255))
        elif level >= 51:
            return ('現実', location, '_re', (0, 153, 255))
        elif level >= 41:
            return ('天堂', location, '_par', (0, 102, 255))
        elif level >= 31:
            return ('地獄', location, '_he', (51, 102, 255))
        elif level >= 21:
            return ('死', 184, '_de', (102, 102, 255))
        elif level >= 11:
            return ('苦', 184, '_pai', (153, 102, 255))
        else:
            return ('快', 184, '_pl', (204, 51, 255))

    async def text_message(self, message, user):
        srs = user['srs']

        out = ''
        out += '"{:s}" of Sect "{:s}"\n'.format(user['name'], user['title'])
        out += 'Level {:d} Apprentice\n'.format(user['level'])
        out += 'Scribed {:d} topics & {:d} posts\n'.format(user['forums']['topics'], user['forums']['posts'])

        out += 'Serving the Crabigator since "{:s}"\n'.format(
            self.parse_date(user['creation_date']))

        out += 'Apprentice: {:d} | Guru: {:d} | Master {:d} | Enlightened {:d} | Burned {:d}\n'.format(
            srs['apprentice'], srs['guru'], srs['master'], srs['enlightened'], srs['burned'])

        # we have additional information through the api
        if user['method'] == 'api':
            rad_cur = user['radicals']['current']
            rad_total = user['radicals']['total']
            kan_cur = user['kanji']['current']
            kan_total = user['kanji']['total']
            out += 'Radicals: {:d}/{:d} ({:.2f}%) | Kanji: {:d}/{:d} ({:.2f}%)\n'.format(
                 rad_cur, rad_total, (rad_cur / rad_total) * 100,
                 kan_cur, kan_total, (kan_cur / kan_total) * 100)

            out += 'Your Next Review: "{:s}"\n'.format(
                 self.parse_date(user['reviews']['next_date']))

            out += 'Lesson Queue: {:d} | Review Queue: {:d}\n'.format(
                 user['lessons']['now'],
                 user['reviews']['now'])

            out += 'Reviews Next Hour: {:d} | Reviews Next Day: {:d}\n'.format(
                 user['reviews']['next_hour'],
                 user['reviews']['next_day'])

        await self.client.send_message(message.channel, '```json\n{:s}\n```'.format(out))

    async def get_user_data(self, message, key=None, username=None):
        user = {
            'method': None,
            'name': '',
            'title': '',
            'avatar': ['', None],
            'level': 0,
            'creation_date': 0,
            'forums': {'posts': 0, 'topics': 0},
            'srs': {
                'apprentice': 0,
                'guru': 0,
                'master': 0,
                'enlightened': 0,
                'burned': 0
            },
            'radicals': {'total': 0, 'current': 0},
            'kanji': {'total': 0, 'current': 0},
            'lessons': {'now': 0},
            'reviews': {'now': 0, 'next_hour': 0, 'next_day': 0, 'next_date': 0},
        }

        srs_dist = None
        lvl_prog = None
        queue = None
        userinfo = None

        # if we have a key, pull data directly from API
        if key:
            url = self.wk_base_url + key

            try:
                srs_dist = requests.get(url + '/srs-distribution').json()
                lvl_prog = requests.get(url + '/level-progression').json()['requested_information']
                queue = requests.get(url + '/study-queue').json()['requested_information']
            except ConnectionError as e:
                self.client.send_message('Failed to get user data.')
                self.log.error('{:s}'.format(e))
                raise e

            userinfo = srs_dist['user_information']
            srs_dist = srs_dist['requested_information']

            user['method'] = 'api'
            user['radicals']['total'] = lvl_prog['radicals_total']
            user['radicals']['current'] = lvl_prog['radicals_progress']
            user['kanji']['total'] = lvl_prog['kanji_total']
            user['kanji']['current'] = lvl_prog['kanji_progress']
            user['lessons']['now'] = queue['lessons_available']
            user['reviews']['now'] = queue['reviews_available']
            user['reviews']['next_hour'] = queue['reviews_available_next_hour']
            user['reviews']['next_day'] = queue['reviews_available_next_day']
            user['reviews']['next_date'] = queue['next_review_date']

        # otherwise if we have a username, pull data from profile page
        elif username:
            page = requests.get('https://www.wanikani.com/community/people/' + username)
            tree = html.fromstring(page.content)

            script = tree.xpath('//div[@class="footer-adjustment"]/script')
            if script != []:
                script = script[0].text.strip()
            else:
                await self.client.send_message(message.channel,
                    "Error while parsing the page, profile not found or doesn't exist")
                return None

            script = script[script.find('var srsCounts'): script.find(
                'Counts.fillInSrsCount(srsCounts.requested_information);')]
            script = script.strip()[16:-1]

            userinfo = json.loads(script)['user_information']
            srs_dist = json.loads(script)['requested_information']
            user['method'] = 'html'
        else:
            return None

        user['name'] = userinfo['username']
        user['title'] = userinfo['title']
        user['level'] = userinfo['level']
        user['avatar'][0] = 'https://www.gravatar.com/avatar/' + userinfo['gravatar']
        user['creation_date'] = userinfo['creation_date']
        user['forums']['posts'] = userinfo['posts_count']
        user['forums']['topics'] = userinfo['topics_count']
        user['srs']['apprentice'] = srs_dist['apprentice']['total']
        user['srs']['guru'] = srs_dist['guru']['total']
        user['srs']['master'] = srs_dist['master']['total']
        user['srs']['enlightened'] = srs_dist['enlighten']['total']
        user['srs']['burned'] = srs_dist['burned']['total']

        try:
            user['avatar'][1] = requests.get(user['avatar'][0]).content
        except ConnectionError as e:
            self.client.send_message('Failed to get user avatar.')
            self.log.error('{:s}'.format(e))

        return user

    async def draw_image(self, message, user):
        rank_category, kanji_loc, ov_color, txt_color = self.get_rank_info(user['level'])

        img_type = 'big' if user['method'] == 'api' else 'small'

        # load images and fonts
        try:
            # TODO: use default avatar image if it could not be downloaded
            ava = Image.open(BytesIO(user['avatar'][1]))
            base = Image.open('{:s}/base_wk_{:s}.png'.format(self.img_base, img_type))
            overlay = Image.open('{:s}/overlay_wk_{:s}{:s}.png'.format(self.img_base, img_type, ov_color))
        except IOError as e:
            self.log.error('{:s}'.format(str(e)))
            raise e

        try:
            font1 = ImageFont.truetype("big_noodle_titling_oblique.ttf", 25)
            font2 = ImageFont.truetype("big_noodle_titling_oblique.ttf", 21)
            font3 = ImageFont.truetype("YuGothB.ttc", 21)
            font4 = ImageFont.truetype("big_noodle_titling_oblique.ttf", 20)
        except OSError as e:
            self.log.error('{:s}'.format(str(e)))
            raise e

        try:
            imgdraw = ImageDraw.Draw(base)
        except IOError as e:
            self.log.error('{:s}'.format(str(e)))
            raise e

        base.paste(ava, (15, 5))
        base.paste(overlay, (0, 0), overlay)

        review_color = (255, 255, 255)
        review_font = font2
        review_pos = (420, 110)

        imgdraw.text((95, 2), '{:s} of sect {:s}'.format(user['name'], user['title']), txt_color, font=font1)
        imgdraw.text((116, 31), str(user['srs']['apprentice']), txt_color, font=font2)
        imgdraw.text((182, 31), str(user['srs']['guru']), txt_color, font=font2)
        imgdraw.text((248, 31), str(user['srs']['master']), txt_color, font=font2)
        imgdraw.text((314, 31), str(user['srs']['enlightened']), txt_color, font=font2)
        imgdraw.text((380, 31), str(user['srs']['burned']), txt_color, font=font2)
        imgdraw.text((95, 60), 'Level: {:d}'.format(user['level']), txt_color, font=font2)

        imgdraw.text((250, 60), 'Joined: {:s}'.format(
            self.parse_date(user['creation_date'], fmt='%B %d, %Y')),
            txt_color, font=font2)

        imgdraw.text((kanji_loc, 61), rank_category, (255, 255, 255), font=font3)

        if user['method'] == 'api':
            imgdraw.text((11, 88), 'Next Review: {:s}'.format(
                self.parse_date(user['reviews']['next_date'])),
                (255, 255, 255), font=font2)

            if int(user['reviews']['now']) > 150:
                review_color = (255, 174, 35)
                review_font = font1
                review_pos = (420, 108)

            imgdraw.text((11, 110), 'Next Hour: {:d}'.format(user['reviews']['next_hour']), (255, 255, 255), font=font4)
            imgdraw.text((136, 110), 'Next Day: {:d}'.format(user['reviews']['next_day']), (255, 255, 255), font=font4)

            imgdraw.text((252, 88), 'Radical: {:d}/{:d}'.format(
                user['radicals']['current'],
                user['radicals']['total']),
                (255, 255, 255), font=font2)

            imgdraw.text((363, 88), 'Kanji: {:d}/{:d}'.format(
                user['kanji']['current'],
                user['kanji']['total']),
                (255, 255, 255), font=font2)

            imgdraw.text((252, 110), 'Lessons: {:d}'.format(user['lessons']['now']), (255, 255, 255), font=font2)
            imgdraw.text((363, 110), 'Reviews: ', (255, 255, 255), font=font2)
            imgdraw.text(review_pos, str(user['reviews']['now']), review_color, font=review_font)

        base.save('cache/ani/wk_' + message.author.id + '.png')
        await self.client.send_file(message.channel, 'cache/ani/wk_' + message.author.id + '.png')
        os.remove('cache/ani/wk_' + message.author.id + '.png')

    async def get_key(self, message, args):
        # if no arguments passed, pulling the ID of a caller
        if not args:
            user_id = str(message.author.id)
        # otherwise see if someone was mentioned
        elif len(message.mentions) > 0:
            user_id = message.mentions[0].id
        # otherwise, pull the username out of a message
        else:
            key = None
            try:
                username = args[0]
            except Exception as e:
                self.log.error(e)
                await self.client.send_message(message.channel, 'Error while parsing the input message')
                return

        if 'username' not in locals():
            if 'user_id' not in locals():
                await self.client.send_message(message.channel, 'No arguments passed')
                return
            # a username was passed
            else:
                query = "SELECT WK_KEY, WK_USERNAME from WANIKANI where USER_ID=?;"
                key_cur = self.db.execute(query, str(user_id))
                db_response = key_cur.fetchone()

                if not db_response:
                    await self.client.send_message(message.channel,
                            'No assigned key or username was found\n'
                            'You can add it by sending me a direct message, for example\n'
                            'For Advanced Stats:\n\t`{0:s}wksave key <your API key>`\nor\n\t`{0:s}wksave username <your username>` for basic stats.'.format(self.prefix))

                    return (None, None)

                key = db_response[0]
                username = db_response[1]

        return (key, username)

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'wanikani'):
            await self.client.send_typing(message.channel)
            cmd_name = 'WaniKani'

            if message.server:
                self.log.info('User %s [%s] on server %s [%s], used the {:s} command on #%s channel'.format(cmd_name),
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            else:
                self.log.info('User %s [%s], used the command.'.format(cmd_name),
                              message.author,
                              message.author.id)

            show_text = False
            args = message.content.split(' ')
            args.pop(0)

            if args and args[-1] == 'text':
                show_text = True
                args.pop()

            key, username = await self.get_key(message, args)

            user = await self.get_user_data(message, key, username)

            if user:
                if show_text:
                    await self.text_message(message, user)
                else:
                    try:
                        await self.draw_image(message, user)
                    except OSError:
                        # failed to generate image
                        await self.text_message(message, user)


class WKKey(Plugin):
    is_global = True
    log = create_logger('wksave')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'wksave'):
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

            try:
                self.log.info(
                    'User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                    message.author,
                    message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)

            try:
                args = message.content[len(pfx) + len('wksave') + 1:]

                mode = args[:args.find(' ')].strip()
                payload = args[args.find(' ') + 1:].strip()  # key or username

                print(args)
                print(mode)
                print(payload)

                if mode == '':
                    await self.client.send_message(message.channel,
                                                   'Bind your Discord profile and your API key or username\n'
                                                   'Usage: `' + pfx + 'wksave' + ' key <your api key here>` or `' + pfx + 'wksave' + ' username <your username here>`')
                    return
                if mode not in ['key', 'username', 'remov']:  # remove
                    await self.client.send_message(message.channel, 'Unknown argument')
                    return
                if mode == 'key':
                    if len(payload) < 32 or len(payload) > 32:
                        await self.client.send_message(message.channel, 'The Key Seems Invalid...')
                        return

                if mode == 'remov':  # remove
                    query = "DELETE from WANIKANI where USER_ID=?;"
                    self.db.execute(query, user_id)
                    self.db.commit()

                    await self.client.send_message(message.channel, 'Record deleted')
                    return

                if mode == 'key':
                    insert_query = "INSERT INTO WANIKANI (USER_ID, WK_KEY) VALUES (?, ?)"
                elif mode == 'username':
                    insert_query = "INSERT INTO WANIKANI (USER_ID, WK_USERNAME) VALUES (?, ?)"
                else:
                    return

                retries = 3
                for i in range(0, retries + 1):
                    try:
                        if i:
                            await self.client.send_message(message.channel, 'Retry {:d}/{:d}'.format(i, retries))

                        self.db.execute(insert_query, user_id, payload)
                        self.db.commit()
                        await self.client.send_message(message.channel, mode.capitalize() + ' Safely Stored. :key:')
                        break
                    except IntegrityError:
                        await self.client.send_message(message.channel,
                                                   'A Key for your User ID already exists, removing...')

                        self.db.rollback()
                        query = "DELETE from WANIKANI where USER_ID=?;"
                        self.db.execute(query, user_id)
                        self.db.commit()

                        continue
                    except UnboundLocalError as e:
                        self.log.error(e)
                        await self.client.send_message(message.channel,
                                                   'There doesn\'t seem to be a key or username tied to you...\nYou can add your it by sending a direct message to me with the WKSave Command, for example:\n`' + pfx + 'wksave' + ' 16813135183151381`\nand just replace the numbers with your WK API Key!')
                    except Exception as e:
                        self.log.error(e)
                        await self.client.send_message(message.channel, 'Something went horribly wrong!')

            except Exception as e:
                self.log.error(e)
                await self.client.send_message(message.channel, 'Error while parsing the input message')


class Jisho(Plugin):
    is_global = True
    log = create_logger('jisho')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'jisho'):
            await self.client.send_typing(message.channel)
            cmd_name = 'Jisho'
            try:
                self.log.info(
                    'User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                    message.author,
                    message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            jisho_q = message.content[len(pfx) + len('jisho') + 1:]
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
