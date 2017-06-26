import pafy
import arrow
import discord
import asyncio
import soundcloud
import time
from sigma.plugins.searches.google.yt_search import search_youtube
from sigma.core.utils import user_avatar
from .playlist_adder import yt_playlist_adder
from .queuebandcamp import queuebandcamp
from config import Prefix, SoundCloudClientID


async def queue(cmd, message, args):
    if message.author.voice:
        if args:
            qry = ' '.join(args)
            if qry.startswith('<'):
                qry = qry[1:]
            if qry.endswith('>'):
                qry = qry[:-1]
            if '?list=' in qry:
                list_id = qry.split('list=')[1].split('&')[0]
                plist = pafy.get_playlist2(list_id)
                item_count = await yt_playlist_adder(message.guild.id, cmd, message.author, plist)
                embed_title = f'ℹ Added {item_count} items from {plist.title}.'
                embed = discord.Embed(color=0x0099FF, title=embed_title)
                await message.channel.send(None, embed=embed)
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
                    elif 'bandcamp.com' in qry:
                        await queuebandcamp(cmd, message, args)
                        return
                    else:
                        response = discord.Embed(color=0xDB0000, title='❗ Unsupported URL Provided')
                        response.set_footer(text='We only support YouTube and SoundCloud for now.')
                        await message.channel.send(None, embed=response)
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
                embed = discord.Embed(color=0x66CC66)
                await cmd.bot.music.add_to_queue(message.guild.id, data)
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
                await message.channel.send(None, embed=embed)
        else:
            q = cmd.bot.music.get_queue(message.guild.id)
            q_bup = asyncio.Queue()
            if q.empty():
                embed = discord.Embed(color=0x0099FF, title='ℹ The Queue Is Empty')
                await message.channel.send(None, embed=embed)
            else:
                q_list = []
                while not q.empty():
                    q_item = await q.get()
                    q_list.append(q_item)
                    await q_bup.put(q_item)
                q_list_mini = q_list[:5]
                cmd.music.queues.update({message.guild.id: q_bup})
                embed = discord.Embed(color=0x0099FF,
                                      title=f'ℹ The {len(q_list_mini)} Upcoming Songs (Total: {len(q_list)})')
                for item in q_list_mini:
                    if item['type'] == 0:
                        information = f'Requested By: {item["requester"].name}\nDuration: {item["sound"].duration}'
                        embed.add_field(name=item['sound'].title, value=f'```\n{information}\n```', inline=False)
                    elif item['type'] == 1:
                        information = f'Requested By: {item["requester"].name}\nDuration: {time.strftime("%H:%M:%S", time.gmtime(item["sound"]["duration"]//1000))}'
                        embed.add_field(name=item['sound']['title'], value=f'```\n{information}\n```', inline=False)
                    elif item['type'] == 2:
                        information = f'Requested By: {item["requester"].name}\nDuration: {time.strftime("%H:%M:%S", time.gmtime(int(item["sound"]["duration"])))}'
                        embed.add_field(name=f"{item['sound']['artist']} - {item['sound']['title']}",
                                        value=f'```\n{information}\n```', inline=False)
                if message.guild.id in cmd.music.repeaters:
                    embed.set_footer(text='The current queue is set to repeat.')
                else:
                    embed.set_footer(text=f'To see the currently playing song type {Prefix}np')
                await message.channel.send(None, embed=embed)
