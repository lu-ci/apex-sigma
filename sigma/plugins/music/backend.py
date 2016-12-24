players = {}


async def get_player(server_id):
    global players
    if server_id not in players:
        player = None
    else:
        player = players[server_id]
    return player


async def player_exists(server_id):
    global players
    if server_id in players:
        return True
    else:
        return False


async def delete_player(server_id):
    global players
    exists = await player_exists(server_id)
    if exists:
        del players[server_id]


async def make_yt_player(server_id, voice, url):
    global players
    exists = await player_exists(server_id)
    if exists:
        player = await get_player(server_id)
        if player.is_playing():
            player.stop()
        await delete_player(server_id)
        player = await voice.create_ytdl_player(url)

    else:
        player = await voice.create_ytdl_player(url)
        players.update({server_id: player})
        print('Created a new player.')
    return player

async def make_local_player(server_id, voice, path):
    global players
    exists = await player_exists(server_id)
    if exists:
        player = await get_player(server_id)
        if player.is_playing():
            player.stop()
        await delete_player(server_id)
        player = voice.create_ffmpeg_player(path)

    else:
        player = voice.create_ffmpeg_player(path)
        players.update({server_id: player})
        print('Created a new player.')
    return player
