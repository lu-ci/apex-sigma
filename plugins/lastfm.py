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
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            lfm_input = message.content[len(pfx) + len(cmd_lfm) + 1:]
            lfm_user, ignore, no_of_songs = lfm_input.partition(' ')
            lfm_url = 'http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user=' + lfm_user + '&api_key=' + lfm_key + '&format=json'
            lfm_data = requests.get(lfm_url).json()
            no_of_songs_in_list = len(lfm_data['toptracks']['track'])
            if no_of_songs == '':
                no_of_songs = 5
            try:
                top_tracks_text = ('Top ' + str(no_of_songs) + ' Tracks for the user `' + lfm_user + '`:\n```')
                for i in range(0, int(no_of_songs)):
                    name = lfm_data['toptracks']['track'][i]['name']
                    artist = lfm_data['toptracks']['track'][i]['artist']['name']
                    top_tracks_text += '\n #' + str(i+1) + ': ' + name + ' by ' + artist
                top_tracks_text += '\n```'
                await self.client.send_message(message.channel, top_tracks_text)
            except:
                try:
                    await self.client.send_message(message.channel, lfm_data['message'])
                except:
                    if no_of_songs_in_list < int(no_of_songs):
                        await self.client.send_message(message.channel,'There are only: `' + str(no_of_songs_in_list) + '` in your list.')
                    else:
                        await self.client.send_message(message.channel, 'We seem to have ran into an error.')
