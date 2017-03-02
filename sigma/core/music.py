import queue as q


class Music(object):
    def __init__(self):
        self.players = {}
        self.queues = {}
        self.volumes = {}
        self.ytdl_params = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
        }

    def get_volume(self, db, sid):
        if sid in self.volumes:
            return self.volumes['sid']
        else:
            return db.get_settings(sid, 'MusicVolume')

    def set_volume(self, db, sid, volume):
        self.volumes.update({sid: volume})
        db.set_settings(sid, 'MusicVolume', volume)

    def get_player(self, sid):
        if sid in self.players:
            return self.players[sid]
        else:
            return None

    def kill_player(self, sid):
        if sid in self.players:
            del self.players[sid]

    def add_to_queue(self, sid, data):
        if sid in self.queues:
            queue = self.queues[sid]
            queue.put(data)
        else:
            queue = q.Queue()
            queue.put(data)
            self.queues.update({sid: queue})

    def get_queue(self, sid):
        if sid in self.queues:
            return self.queues[sid]
        else:
            return None

    def get_from_queue(self, sid):
        if sid in self.queues:
            return self.queues[sid].get()
        else:
            return None

    async def make_yt_player(self, sid, voice, url):
        player = await voice.create_ytdl_player(url, ytdl_options=self.ytdl_params)
        self.players.update({sid: player})
