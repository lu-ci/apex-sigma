import pafy
import arrow
import discord
import asyncio
from sigma.plugins.searches.google.yt_search import search_youtube
from sigma.core.utils import user_avatar
from .playlist_adder import playlist_adder
from config import Prefix


async def queue(cmd, message, args):
    if message.author.voice_channel:
        if args:
            qry = ' '.join(args)
            if '?list=' in qry:
                list_id = qry.split('list=')[1]
                list_url = 'https://www.youtube.com/playlist?list=' + list_id
                plist = pafy.get_playlist(list_url)
                item_count = len(plist['items'])
                embed_title = f'ℹ Playlist Detected. Adding {item_count} items...'
                embed = discord.Embed(color=0x0099FF, title=embed_title)
                await cmd.bot.send_message(message.channel, None, embed=embed)
                await playlist_adder(message.server.id, cmd.music, message.author, plist)
                await asyncio.sleep(3)
            else:
                if qry.startswith('https://'):
                    video_url = qry
                else:
                    video_url = await search_youtube(qry)
                video = pafy.new(video_url)
                data = {
                    'url': video_url,
                    'requester': message.author,
                    'video': video,
                    'timestamp': arrow.now().timestamp
                }
                total = arrow.now().timestamp
                curr_queue = cmd.music.get_queue(message.server.id)
                if curr_queue:
                    for item in list(curr_queue.queue):
                        h, m, s = item['video'].duration.split(':')
                        addition = int(s) + (int(m) * 60) + (int(h) * 3600)
                        total += addition
                time_data = arrow.utcnow().fromtimestamp(total).naive
                embed = discord.Embed(color=0x66CC66, timestamp=time_data)
                cmd.bot.music.add_to_queue(message.server.id, data)
                embed.add_field(name='✅ Added To Queue', value=video.title)
                embed.set_thumbnail(url=video.thumb)
                embed.set_author(name=f'{message.author.name}#{message.author.discriminator}',
                                 icon_url=user_avatar(message.author))
                embed.set_footer(text=f'Duration: {video.duration}')
                await cmd.bot.send_message(message.channel, None, embed=embed)
        else:
            q = cmd.bot.music.get_queue(message.server.id)
            if q.empty():
                embed = discord.Embed(color=0x0099FF, title='ℹ The Queue Is Empty')
                await cmd.bot.send_message(message.channel, None, embed=embed)
            else:
                q_list = list(q.queue)[:5]
                q_text = ''
                for item in q_list:
                    q_text += f'\n{item["video"].title}'
                embed = discord.Embed(color=0x0099FF)
                embed.add_field(name=f'ℹ {len(q_list)} Upcoming Songs (Total: {len(list(q.queue))})',
                                value=f'```\n{q_text}\n```', inline=False)
                embed.set_footer(text=f'To see the currently playing song type {Prefix}np')
                await cmd.bot.send_message(message.channel, None, embed=embed)
