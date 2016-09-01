from plugin import Plugin
from config import cmd_jisho
from config import cmd_wk
from utils import create_logger
from utils import bold
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
            key = message.content[len(pfx) + len(cmd_wk) + 1:]
            url = 'https://www.wanikani.com/api/user/' + key + '/srs-distribution'
            api = requests.get(url).json()
            try:
                username = api['user_information']['username']
                title = api['user_information']['title']
                level = str(api['user_information']['level'])
                creation_date = datetime.datetime.fromtimestamp(api['user_information']['creation_date']).strftime('%B %d, %Y')
                topics_count = str(api['user_information']['topics_count'])
                posts_count = str(api['user_information']['posts_count'])

                apprentice = 'Apprentice: ' + bold(str(api['requested_information']['apprentice']['total']))
                guru = 'Guru: ' + bold(str(api['requested_information']['guru']['total']))
                master = 'Master: ' + bold(str(api['requested_information']['master']['total']))
                enlightned = 'Enlightened: ' + bold(str(api['requested_information']['enlighten']['total']))
                burned = 'Burned: ' + bold(str(api['requested_information']['burned']['total']))

                out = ''
                out += bold(username) + ' of ' + bold('Sect ' + title) + '\n'
                out += bold('Level ' + level) + ' Apprentice' + '\n'
                out += 'Scribed ' + bold(topics_count + ' topics') + ' & ' + bold(posts_count + ' posts') + '\n'
                out += 'Serving the Crabigator since ' + bold(creation_date) + '\n'
                out += apprentice + ' | ' + guru + ' | ' + master + ' | ' + enlightned + ' | ' + burned
                await self.client.send_message(message.channel, out)
            except:
                await self.client.send_message(message.channel, 'Something went wrong ¯\_(ツ)_/¯')


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
