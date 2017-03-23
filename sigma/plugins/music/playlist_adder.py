import arrow


def playlist_adder(sid, cmd, req, playlist_obj):
    music = cmd.music
    counter = 0
    for item in playlist_obj:
        hour, minute, second = item.duration.split(':')
        total_time = (int(hour) * 3600) + (int(minute) * 60) + int(second)
        if total_time <= 600:
            counter += 1
            data = {
                'url': 'https://www.youtube.com/watch?v=' + item.videoid,
                'requester': req,
                'video': item,
                'timestamp': arrow.now().timestamp
            }
            music.add_to_queue(sid, data)
        if counter >= 200:
            break
    return counter
