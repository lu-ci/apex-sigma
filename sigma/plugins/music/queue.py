import pafy
import discord
from sigma.plugins.searches.google.yt_search import search_youtube
from sigma.core.utils import user_avatar


async def queue(cmd, message, args):
    if message.author.voice_channel:
        if args:
            qry = ' '.join(args)
            if 'list=' in qry:
                embed = discord.Embed(color=0xDB0000, title=':no_entry: Playlist Links Are Not Allowed.')
                await cmd.bot.send_message(message.channel, None, embed=embed)
                return
            if qry.startswith('https://'):
                video_url = qry
            else:
                video_url = search_youtube(qry)
            video = pafy.new(video_url)
            data = {
                'url': video_url,
                'requester': message.author,
                'video': video
            }
            cmd.bot.music.add_to_queue(message.server.id, data)
            embed = discord.Embed(color=0x66CC66)
            embed.add_field(name=':white_check_mark: Added To Queue', value=video.title)
            embed.set_thumbnail(url=video.thumb)
            embed.set_author(name=f'{message.author.name}#{message.author.discriminator}',
                             icon_url=user_avatar(message.author))
            embed.set_footer(text=f'Duration: {video.duration}')
            await cmd.bot.send_message(message.channel, None, embed=embed)
        else:
            q = cmd.bot.music.get_queue(message.server.id)
            if q.empty():
                embed = discord.Embed(color=0x0099FF, title=':information_source: The Queue Is Empty')
                await cmd.bot.send_message(message.channel, None, embed=embed)
            else:
                q_list = list(q.queue)[:5]
                q_text = ''
                for item in q_list:
                    q_text += f'\n{item["video"].title}'
                embed = discord.Embed(color=0x0099FF)
                embed.add_field(name=':information_source: Items In The Queue', value=f'```\n{q_text}\n```', inline=False)
                await cmd.bot.send_message(message.channel, None, embed=embed)
