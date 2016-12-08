from apiclient import discovery
from config import GoogleAPIKey
from .backend import play_yt

async def play(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, 'No arguments provided, provide a YouTube link or Keyword Search.')
        return
    if cmd.bot.is_voice_connected(message.server):
        voice = cmd.bot.voice_client_in(message.server)
    else:
        voice = await cmd.bot.join_voice_channel(message.author.voice_channel)
    request = ' '.join(args)
    if request.startswith('https://you'):
        pl = await play_yt(voice, request)
        video_name = pl.title()
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
        await play_yt(voice, video_url)
    await cmd.bot.send_message(message.channel, 'Playing **' + video_name + '**')
