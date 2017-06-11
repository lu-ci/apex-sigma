import aiohttp
import json
import arrow
import pafy
import discord
from config import MashapeKey
from sigma.plugins.searches.google.yt_search import search_youtube


async def queuedeezerplaylist(cmd, message, args):
    if args:
        initial_response = discord.Embed(color=0xFFCC66, title='💽 Processing...')
        init_resp_msg = await message.channel.send(embed=initial_response)
        playlist_id = ''.join(args)
        api_url = f'https://deezerdevs-deezer.p.mashape.com/playlist/{playlist_id}'
        headers = {'X-Mashape-Key': MashapeKey, 'Accept': 'text/plain'}
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, headers=headers) as data:
                data = await data.read()
                data = json.loads(data)
        playlist_name = data['title']
        playlist_items = data['tracks']['data']
        detection_response = discord.Embed(color=0xFFCC66,
                                           title=f'💽 Importing {len(playlist_items)} songs from {playlist_name}...')
        await init_resp_msg.edit(embed=detection_response)
        for song in playlist_items:
            qry = f'{song["artist"]["name"]} {song["title"]}'
            song_url = await search_youtube(qry)
            sound = pafy.new(song_url)
            sound_type = 0
            data = {
                'url': song_url,
                'type': sound_type,
                'requester': message.author,
                'sound': sound,
                'timestamp': arrow.now().timestamp
            }
            await cmd.bot.music.add_to_queue(message.guild.id, data)
        finished_response = discord.Embed(color=0xFFCC66,
                                          title=f'💽 All Done! {len(playlist_items)} songs were imported!')
        await init_resp_msg.edit(embed=finished_response)
    else:
        response = discord.Embed(color=0x696969, title=f'🔍 Nothing Inputted.')
        await message.channel.send(embed=response)
