import queue as q

ytdl_params = {
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
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

class Music(object):
    def __init__(self):
        self.players = {}
        self.queues = {}
        self.volumes = {}

    def get_volume(self, sid):
        if sid in self.volumes:
            return self.volumes['sid']
        else:
            return 100

    def set_volume(self, sid, volume):
        self.volumes.update({sid: volume})

    async def get_player(self, cmd, message):
        if message.server.id in self.players:
            return self.players['sid']
        else:
            data = self.queues
            url = data['url']
            voice = cmd.bot.voice_client_in(message.server)
            if not voice:
                voice = await cmd.bot.join_voice_channel(message.author.voice_channel)
            player = voice.create_ytdl_player(url, ytdl_options=ytdl_params)
            self.players.update({message.server.id: player})
            return self.players['sid']

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
