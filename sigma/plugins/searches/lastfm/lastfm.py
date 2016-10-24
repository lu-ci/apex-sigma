import requests

from config import LastFMAPIKey


async def lastfm(cmd, message, args):
    lfm_input = ' '.join(args)

    lfm_user, ignore, no_of_songs = lfm_input.partition(' ')
    lfm_url = 'http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user=' + lfm_user + '&api_key=' + LastFMAPIKey + '&format=json'
    lfm_data = requests.get(lfm_url).json()
    no_of_songs_in_list = len(lfm_data['toptracks']['track'])

    if no_of_songs == '':
        no_of_songs = 5

    try:
        top_tracks_text = ('Top ' + str(no_of_songs) + ' Tracks for the user `' + lfm_user + '`:\n```')

        for i in range(0, int(no_of_songs)):
            name = lfm_data['toptracks']['track'][i]['name']
            artist = lfm_data['toptracks']['track'][i]['artist']['name']
            top_tracks_text += '\n #' + str(i + 1) + ': ' + name + ' by ' + artist

        top_tracks_text += '\n```'
        await cmd.reply(top_tracks_text)
    except Exception:
        try:
            await cmd.reply(lfm_data['message'])
        except Exception as e:
            if no_of_songs_in_list < int(no_of_songs):
                await cmd.reply('There are only: `' + str(no_of_songs_in_list) + '` in your list.')
            else:
                cmd.log.error(e)
                await cmd.reply('We seem to have ran into an error.')
