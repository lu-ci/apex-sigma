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
            player = cmd.bot.music.get_player(message.server.id)
            if player:
                if player.is_playing():
                    embed = discord.Embed(
                        title=':warning: Already playing in ' + cmd.bot.voice_client_in(message.server).channel.name,
                        color=0xFF9900)
                    await cmd.bot.send_message(message.channel, None, embed=embed)
                    return
            voice_instance = cmd.bot.voice_client_in(message.server)
            if voice_instance:
                pass
            else:
                voice_instance = await cmd.bot.join_voice_channel(message.author.voice_channel)
            while not queue.empty():
                item = queue.get()
                video = item['video']
                await cmd.bot.music.make_player(message.server.id, voice_instance, item['url'])
                player = cmd.bot.music.get_player(message.server.id)
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
