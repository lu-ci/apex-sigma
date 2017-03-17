import pafy
import os
import queue as q


class Music(object):
    def __init__(self):
        self.players = {}
        self.initializing = []
        self.queues = {}
        self.volumes = {}
        self.currents = {}
        self.ytdl_params = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': '%(id)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0'
        }

    def get_volume(self, db, sid):
        if sid in self.volumes:
            return self.volumes[sid]
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
            queue = q.Queue()
            self.queues.update({sid: queue})
            return queue

    def get_from_queue(self, sid):
        if sid in self.queues:
            return self.queues[sid].get()
        else:
            return None

    def purge_queue(self, sid):
        if sid in self.queues:
            self.queues[sid] = q.Queue()

    @staticmethod
    def download_data(url):
        output = 'cache/'
        video = pafy.new(url)
        audio = video.getbestaudio()
        file_location = output + video.videoid
        if not os.path.exists(file_location):
            audio.download(file_location)
        return file_location

    async def make_player(self, sid, voice, location):
        if ('youtu' and 'https') in location:
            file_location = self.download_data(location)
        else:
            file_location = location
        player = voice.create_ffmpeg_player(file_location)
        self.players.update({sid: player})

    def add_init(self, sid):
        self.initializing.append(sid)

    def remove_init(self, sid):
        self.initializing.remove(sid)
