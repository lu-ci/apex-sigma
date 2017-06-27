import aiohttp
import re
import json


async def parse_bandcamp_album(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as dl_data:
            r = await dl_data.text()
    start = r.find('var TralbumData')
    end = r.find('};', start) + 2
    tr_album_data = r[start:end]
    tr_album_data = tr_album_data[18:-1]
    tr_album_data = re.sub(r'//\s.*\n', '\n', tr_album_data)
    tr_album_data = re.compile(r'.*:\s').sub(lambda match: '"{}":'.format(match.group().strip()[:-1]), tr_album_data)
    start = tr_album_data.find('"url"')
    end = tr_album_data.find('\n', tr_album_data.find('"url"'))
    url = tr_album_data[start:end]
    formatted_url = url[7:-2]
    if formatted_url.find('" + "') == -1:
        formatted_url = formatted_url.split('/track/')
        formatted_url[1] = '/track/' + formatted_url[1]
    else:
        formatted_url = formatted_url.replace('"', '').replace(' ', '').split('+')
    formatted_url = '"url_base":"{}",\n"url_album":"{}",'.format(formatted_url[0], formatted_url[1])
    tr_album_data = tr_album_data.replace(url, formatted_url)
    tr_album_data = json.loads(tr_album_data)  # parsing as JSON
    tracks = []
    for track in tr_album_data['trackinfo']:
        tracks.append({
            'id': track['track_id'],
            'thumbnail': 'https://f4.bcbits.com/img/a{}_16.jpg'.format(tr_album_data['art_id']),
            'artist': tr_album_data['artist'],
            'title': track['title'],
            'duration': track['duration'],
            'file': 'http:' + track['file']['mp3-128'],
            'url': tr_album_data['url_base'] + track['title_link']
        })
    return tracks
