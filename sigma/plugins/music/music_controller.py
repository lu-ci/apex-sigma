import asyncio

players = {}
queues = {}


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


def del_player(server):
    if server.id in players:
        del players[server.id]


def del_from_queue(server, order_number):
    if server.id in queues:
        queue = queues[server.id]
        queue.remove(order_number)


def purge_queue(server):
    if server.id in queues:
        del queues[server.id]


def add_to_queue(server, requester, player_type, address):
    if server.id in queues:
        queue = queues[server.id]
    else:
        queue = []
    queue_data = {
        'Type': player_type,
        'Requester': requester,
        'Location': address
    }
    queue.append(queue_data)
    queues.update({server.id: queue})


async def make_yt_player(server, voice, url):
    player = await voice.create_ytdl_player(url)
    players.update({server.id: player})
