players = {}
queues = {}
volumes = {}
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


def get_player(server):
    if server.id in players:
        return players[server.id]
    else:
        return None


def get_queue(server):
    if server.id in queues:
        return queues[server.id]
    else:
        return []


def get_volume(server):
    if server.id in volumes:
        return volumes[server.id]
    else:
        return None


def set_volume(server, volume):
    volumes.update({server.id: volume})


def del_player(server):
    if server.id in players:
        del players[server.id]


def del_from_queue(server, order_number):
    if server.id in queues:
        queue = queues[server.id]
        item = queue[order_number]
        queue.remove(item)


def purge_queue(server):
    if server.id in queues:
        del queues[server.id]


def add_to_queue(server, requester, player_type, address, title):
    if server.id in queues:
        queue = queues[server.id]
    else:
        queue = []
    queue_data = {
        'Type': player_type,
        'Requester': requester,
        'Location': address,
        'Title': title
    }
    queue.append(queue_data)
    queues.update({server.id: queue})


async def make_yt_player(server, voice, url):
    try:
        player = await voice.create_ytdl_player(url, ytdl_options=ytdl_params)
        players.update({server.id: player})
    except:
        pass
