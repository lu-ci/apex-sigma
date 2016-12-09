from apiclient import discovery
from config import GoogleAPIKey
from .backend import get_player, make_yt_player, player_exists, delete_player


async def play(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, 'No arguments provided, provide a YouTube link or Keyword Search.')
        return
    if cmd.bot.is_voice_connected(message.server):
        voice = cmd.bot.voice_client_in(message.server)
    else:
        try:
            voice = await cmd.bot.join_voice_channel(message.author.voice_channel)
        except:
            cmd.bot.send_message(message.channel, 'You are not in a voice channel.')
            return
    request = ' '.join(args)
    if request.startswith('https://'):
        existence = await player_exists(message.server.id)
        if existence:
            player = await make_yt_player(message.server.id, voice, request)
            player.start()
        else:
            player = await make_yt_player(message.server.id, voice, request)
            player.start()
        try:
            video_name = player.title()
        except:
            video_name = 'Playlist'
        player.start()
    else:
        youtube = discovery.build('youtube', 'v3', developerKey=GoogleAPIKey)
        search_response = youtube.search().list(q=request, part='id,snippet').execute()
        video_id = None
        video_name = None
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                video_id = search_result["id"]["videoId"]
                video_name = search_result["snippet"]["title"]
                break
        video_url = "https://www.youtube.com/watch?v=" + video_id
        existence = await player_exists(message.server.id)
        if existence:
            player = await make_yt_player(message.server.id, voice, video_url)
            player.start()
        else:
            player = await make_yt_player(message.server.id, voice, video_url)
            player.start()

    await cmd.bot.send_message(message.channel, 'Playing **' + video_name + '**')
