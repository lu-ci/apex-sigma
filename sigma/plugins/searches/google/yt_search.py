from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from config import GoogleAuthFileLocation


def search_youtube(query):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(GoogleAuthFileLocation)
    service_name = "youtube"
    version = "v3"
    youtube = discovery.build(service_name, version, credentials=credentials)
    search_response = youtube.search().list(q=query, part='id,snippet').execute()
    video_id = None
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            video_id = search_result["id"]["videoId"]
            break
    video_url = "https://www.youtube.com/watch?v=" + video_id
    return video_url
