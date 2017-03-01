import discord
import asyncio
from sigma.core.utils import user_avatar


async def play(cmd, message, args):
    if message.author.voice_channel:
        queue = cmd.bot.music.get_queue(message.server.id)
        if not queue or queue.empty():
            embed = discord.Embed(color=0xFF9900, title=':warning: The Queue Is Empty')
            await cmd.bot.send_message(message.channel, None, embed=embed)
        else:
            while not queue.empty():
                item = queue.get()
                player = cmd.bot.music.get_player(message.server.id)
                if player:
                    if player.is_playing():
                        return
                else:
                    voice = cmd.bot.voice_client_in(message.server)
                    if not voice:
                        voice = await cmd.bot.join_voice_channel(message.author.voice_channel)
                    player = await voice.create_ytdl_player(item['url'], ytdl_options=cmd.bot.music.ytdl_params)
                video = item['video']
                embed = discord.Embed(color=0x0099FF)
                embed.add_field(name='🎵 Now Playing', value=video.title)
                embed.set_thumbnail(url=video.thumb)
                embed.set_author(name=f'{message.author.name}#{message.author.discriminator}',
                                 icon_url=user_avatar(item['requester']))
                embed.set_footer(text=f'Duration: {video.duration}')
                await cmd.bot.send_message(message.channel, None, embed=embed)
                player.start()
                while not player.is_done():
                    asyncio.sleep(2)
                cmd.bot.music.kill_player(message.server.id)
