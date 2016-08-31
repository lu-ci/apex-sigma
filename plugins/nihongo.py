from plugin import Plugin
from config import cmd_jisho, cmd_wk
from utils import create_logger
import datetime
import requests


class WK(Plugin):
    is_global = True
    log = create_logger(cmd_wk)

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_wk):
            await self.client.send_typing(message.channel)
            cmd_name = 'WaniKani'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            wk_key = message.content[len(pfx) + len(cmd_wk) + 1:]
            profile_url = requests.get('https://www.wanikani.com/api/user/' + wk_key + '/study-queue').json()
            progress_url = requests.get('https://www.wanikani.com/api/user/' + wk_key + '/level-progression').json()
            srs_url = requests.get('https://www.wanikani.com/api/user/' + wk_key + '/srs-distribution').json()
            try:
                username = profile_url['user_information']['username']
                level = profile_url['user_information']['level']
                title = profile_url['user_information']['title']
                about = profile_url['user_information']
                if about == '':
                    about = 'Nothing written.'
                website = profile_url['user_information']['website']
                twitter = profile_url['user_information']['twitter']
                topics = str(profile_url['user_information']['topics_count'])
                print(topics)
                posts = str(profile_url['user_information']['posts_count'])
                print(posts)
                join_date_raw = profile_url['user_information']['creation_date']
                join_date = str(datetime.datetime.fromtimestamp(join_date_raw).strftime('%Y-%m-%d %H:%M:%S'))
                print(join_date)
                vac_date_raw = profile_url['user_information']['vacation_date']
                vac_date = str(datetime.datetime.fromtimestamp(join_date_raw).strftime('%Y-%m-%d %H:%M:%S'))
                print(vac_date)
                lessons_count = str(profile_url['requested_information']['lessons_available'])
                print(lessons_count)
                reviews_count = str(profile_url['requested_information']['reviews_available'])
                print(reviews_count)
                next_review = str(datetime.datetime.fromtimestamp(
                    profile_url['requested_information']['next_review_date']).strftime(
                    '%Y-%m-%d %H:%M:%S'))
                print(next_review)
                rad_prog = progress_url['requested_information']['radicals_progress']
                rad_total = str(progress_url['requested_information']['radicals_total'])
                print(rad_total)
                kanji_prog = progress_url['requested_information']['kanji_progress']
                kanji_total = str(progress_url['requested_information']['kanji_total'])
                print(kanji_total)
                stats_text = str('\nName: ' + username +
                            ' Level: ' + level +
                            '\nAbout: ' + about +
                            '\nTopics: ' + topics +
                            ' Posts: ' + posts +
                            '\nJoin Date: ' + join_date +
                            '\nVacation: ' + vac_date +
                            '\nLessons: ' + lessons_count +
                            ' Reviews: ' + reviews_count +
                            '\nNext Review: ' + next_review +
                            '\nRadicals: ' + rad_total +
                            '\nKanji: ' + kanji_total +
                            '\n```')
                await self.client.send_message(message.channel, stats_text)
            except SyntaxError:
                await self.client.send_message(message.channel, 'The key is wrong or the API dun goofed.')


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
                    is_common = str(request['data'][0]['is_common']).title()
                except:
                    is_common = 'False'
                try:
                    ja_word = request['data'][0]['japanese'][0]['word']
                except:
                    ja_word = 'None'
                try:
                    ja_reading = request['data'][0]['japanese'][0]['reading']
                except:
                    ja_reading = 'None'
                try:
                    eng_def = request['data'][0]['senses'][0]['english_definitions'][0]
                except:
                    eng_def = 'None'
                try:
                    info = request['data'][0]['senses'][0]['info'][0]
                except:
                    info = 'None'
                try:
                    tags = request['data'][0]['tags'][0]
                except:
                    tags = 'None'
                result_text = ('Search querry for `' + jisho_q + '`:\n```' +
                               '\nJapanese Word: ' + ja_word +
                               '\nJapanese Reading: ' + ja_reading +
                               '\nEnglish Definition: ' + eng_def +
                               '\nInfo: ' + info +
                               '\nCommon word: ' + is_common +
                               '\nTags: ' + tags + '\n```')
                await self.client.send_message(message.channel, result_text)
            except:
                await self.client.send_message(message.channel, 'The word was not found or the API dun goofed.')
