import aiohttp
import re


async def search_youtube(query):
    url_base = "https://www.youtube.com/results?"
    params = {
        "q": query
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{url_base}', params=params) as data:
            html_content = await data.text()
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content)
            video_url = f'https://www.youtube.com/watch?v={search_results[0]}'
    return video_url
