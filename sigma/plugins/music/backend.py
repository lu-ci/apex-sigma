async def play_yt(voice, url):
    player = await voice.create_ytdl_player(url)
    player.start()
    return player
