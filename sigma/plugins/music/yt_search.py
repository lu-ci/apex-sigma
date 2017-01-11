from apiclient import discovery
from oauth2client.client import GoogleCredentials
from config import GoogleAPIKey


def search_youtube(query):
    credentials = GoogleCredentials.get_application_default()
    youtube = discovery.build('youtube', 'v3', credentials=credentials)
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
