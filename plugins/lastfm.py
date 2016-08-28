from plugin import Plugin
from config import cmd_lfm
from config import LastFMAPIKey as lfm_key
from utils import create_logger
import requests

class LastFM(Plugin):
    is_global = True
    log = create_logger(cmd_lfm)

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_lfm + ' '):
            await self.client.send_typing(message.channel)
            cmd_name = 'LastFM'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            lfm_input = message.content[len(pfx) + len(cmd_lfm) + 1:]
            lfm_user, ignore, no_of_songs = lfm_input.partition(' ')
            lfm_url = 'http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user=' + lfm_user + '&api_key=' + lfm_key + '&format=json'
            lfm_data = requests.get(lfm_url).json()
            no_of_songs_in_list = len(lfm_data['toptracks']['track'])
            try:
                tr1_n = lfm_data['toptracks']['track'][0]['name']
                tr1_a = lfm_data['toptracks']['track'][0]['artist']['name']
                tr2_n = lfm_data['toptracks']['track'][1]['name']
                tr2_a = lfm_data['toptracks']['track'][1]['artist']['name']
                tr3_n = lfm_data['toptracks']['track'][2]['name']
                tr3_a = lfm_data['toptracks']['track'][2]['artist']['name']
                tr4_n = lfm_data['toptracks']['track'][3]['name']
                tr4_a = lfm_data['toptracks']['track'][3]['artist']['name']
                tr5_n = lfm_data['toptracks']['track'][4]['name']
                tr5_a = lfm_data['toptracks']['track'][4]['artist']['name']
                top_tracks_text = ('Top 5 Tracks for the user `' + lfm_user + '`:\n```' +
                                   '\n #1: ' + tr1_n + ' by ' + tr1_a +
                                   '\n #2: ' + tr2_n + ' by ' + tr2_a +
                                   '\n #3: ' + tr3_n + ' by ' + tr3_a +
                                   '\n #4: ' + tr4_n + ' by ' + tr4_a +
                                   '\n #5: ' + tr5_n + ' by ' + tr5_a +
                                   '\n```')
                await self.client.send_message(message.channel, top_tracks_text)
            except:
                try:
                    await self.client.send_message(message.channel, lfm_data['message'])
                except:
                    #try:
                        #await self.client.send_message(message.channel,'There are only: `' + str(no_of_songs_in_list) + '` in your list.')
                    #except:
                        await self.client.send_message(message.channel, 'We seem to have ran into an error.')
