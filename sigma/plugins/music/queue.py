import pafy
import arrow
import discord
import asyncio
import soundcloud
from sigma.plugins.searches.google.yt_search import search_youtube
from sigma.core.utils import user_avatar
from .playlist_adder import yt_playlist_adder
from config import Prefix, SoundCloudClientID


async def queue(cmd, message, args):
    if message.author.voice_channel:
        if args:
            qry = ' '.join(args)
            if '?list=' in qry:
                list_id = qry.split('list=')[1].split('&')[0]
                plist = pafy.get_playlist2(list_id)
                item_count = yt_playlist_adder(message.server.id, cmd, message.author, plist)
                embed_title = f'ℹ Added {item_count} items from {plist.title}.'
                embed = discord.Embed(color=0x0099FF, title=embed_title)
                await cmd.bot.send_message(message.channel, None, embed=embed)
                await asyncio.sleep(3)
            else:
                if qry.startswith('https://'):
                    if 'youtu' in qry:
                        song_url = qry
                        sound = pafy.new(song_url)
                        sound_type = 0
                    elif 'soundcloud' in qry:
                        song_url = qry
                        sc_cli = soundcloud.Client(client_id=SoundCloudClientID)
                        sound = sc_cli.get('/resolve', url=qry).fields()
                        sound_type = 1
                    else:
                        response = discord.Embed(color=0xDB0000, title='❗ Unsupported URL Provided')
                        response.set_footer(text='We only support YouTube and SoundCloud for now.')
                        return
                else:
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
                if sound_type == 0:
                    embed.add_field(name='✅ Added To Queue', value=sound.title)
                    embed.set_thumbnail(url=sound.thumb)
                    embed.set_author(name=f'{message.author.name}#{message.author.discriminator}',
                                     icon_url=user_avatar(message.author))
                    embed.set_footer(text=f'Duration: {sound.duration}')
                elif sound_type == 1:
                    embed.add_field(name='✅ Added To Queue', value=sound['title'])
                    embed.set_thumbnail(url=sound['artwork_url'])
                    embed.set_author(name=f'{message.author.name}#{message.author.discriminator}',
                                     icon_url=user_avatar(message.author))
                else:
                    return
                await cmd.bot.send_message(message.channel, None, embed=embed)
        else:
            q = cmd.bot.music.get_queue(message.server.id)
            if q.empty():
                embed = discord.Embed(color=0x0099FF, title='ℹ The Queue Is Empty')
                await cmd.bot.send_message(message.channel, None, embed=embed)
            else:
                q_list = list(q.queue)[:5]
                embed = discord.Embed(color=0x0099FF,
                                      title=f'ℹ The {len(q_list)} Upcoming Songs (Total: {len(list(q.queue))})')
                for item in q_list:
                    information = f'Requested By: {item["requester"].name}\nDuration: {item["video"].duration}'
                    embed.add_field(name=item['video'].title, value=f'```\n{information}\n```', inline=False)
                embed.set_footer(text=f'To see the currently playing song type {Prefix}np')
                await cmd.bot.send_message(message.channel, None, embed=embed)
