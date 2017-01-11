from apiclient import discovery
from config import GoogleAPIKey


def search_youtube(query):
    youtube = discovery.build('youtube', 'v3', developerKey=GoogleAPIKey)
    search_response = youtube.search().list(q=query, part='id,snippet').execute()
    video_id = None
    video_name = None
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            video_id = search_result["id"]["videoId"]
            video_name = search_result["snippet"]["title"]
            break
    video_url = "https://www.youtube.com/watch?v=" + video_id
    return video_url, video_id, video_name
