import pafy
import os
import hashlib
import soundcloud
import discord
import aiohttp
import asyncio
from config import SoundCloudClientID


class Music(object):
    def __init__(self):
        self.initializing = []
        self.queues = {}
        self.item_lists = {}
        self.volumes = {}
        self.currents = {}
        self.repeaters = []
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

    async def add_to_queue(self, sid, data):
        if sid in self.queues:
            queue = self.queues[sid]
            await queue.put(data)
        else:
            queue = asyncio.Queue()
            await queue.put(data)
            self.queues.update({sid: queue})

    def get_queue(self, sid):
        if sid in self.queues:
            return self.queues[sid]
        else:
            queue = asyncio.Queue()
            self.queues.update({sid: queue})
            return queue

    async def get_from_queue(self, sid):
        if sid in self.queues:
            return await self.queues[sid].get()
        else:
            return None

    def purge_queue(self, sid):
        if sid in self.queues:
            self.queues[sid] = asyncio.Queue()

    @staticmethod
    def download_yt_data(url):
        output = 'cache/'
        video = pafy.new(url)
        audio = video.getbestaudio()
        file_location = output + video.videoid
        if not os.path.exists(file_location):
            audio.download(file_location, quiet=True)
        return file_location

    @staticmethod
    async def download_sc_data(url):
        output = 'cache/'
        sc_cli = soundcloud.Client(client_id=SoundCloudClientID)
        data = sc_cli.get('/resolve', url=url)
        stream_url = sc_cli.get(data.stream_url, allow_redirects=False)
        crypt = hashlib.new('md5')
        crypt.update(str(data.fields()['id']).encode('utf-8'))
        filename = crypt.hexdigest()
        file_location = output + filename
        if not os.path.exists(file_location):
            with open(file_location, 'wb') as data_file:
                async with aiohttp.ClientSession() as session:
                    async with session.get(stream_url.location) as dl_data:
                        total_data = await dl_data.read()
                        data_file.write(total_data)
        return file_location

    async def make_player(self, voice, item):
        location = item['url']
        if item['type'] == 0:
            file_location = self.download_yt_data(location)
        elif item['type'] == 1:
            file_location = await self.download_sc_data(location)
        else:
            file_location = location
        source = discord.FFmpegPCMAudio(file_location, executable='ffmpeg')
        voice.play(source)

    def add_init(self, sid):
        self.initializing.append(sid)

    def remove_init(self, sid):
        self.initializing.remove(sid)
