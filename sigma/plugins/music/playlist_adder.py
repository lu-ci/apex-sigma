import arrow


async def playlist_adder(sid, music, req, playlist_obj):
    for item in playlist_obj['items']:
        item = item['pafy']
        data = {
            'url': 'https://www.youtube.com/watch?v=' + item.videoid,
            'requester': req,
            'video': item,
            'timestamp': arrow.now().timestamp
        }
        music.add_to_queue(sid, data)
