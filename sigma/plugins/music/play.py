import discord
import asyncio
from sigma.core.utils import user_avatar
from .init_clock import init_clock


async def play(cmd, message, args):
    if args:
        task = cmd.bot.plugin_manager.commands['queue'].call(message, args)
        cmd.bot.loop.create_task(task)
        if message.guild.id in cmd.music.voices:
            bot_voice = cmd.music.voices[message.guild.id]
            if bot_voice.is_playing():
                return
        await asyncio.sleep(3)
    if message.guild.id not in cmd.music.initializing:
        if not message.author.voice:
            embed = discord.Embed(
                title='⚠ I don\'t see you in a voice channel', color=0xFF9900)
            await message.channel.send(None, embed=embed)
            return
        srv_queue = cmd.music.get_queue(message.guild.id)
        if len(srv_queue.queue) == 0:
            embed = discord.Embed(
                title='⚠ The queue is empty', color=0xFF9900)
            await message.channel.send(None, embed=embed)
            return
        cmd.music.add_init(message.guild.id)
        cmd.bot.loop.create_task(init_clock(cmd.music, message.guild.id))
        if message.guild.id in cmd.music.voices:
            bot_voice = cmd.music.voices[message.guild.id]
        else:
            bot_voice = None
        if not bot_voice:
            try:
                bot_voice = await message.author.voice.channel.connect()
                cmd.music.voices.update({message.guild.id: bot_voice})
                embed = discord.Embed(title='✅ Joined ' + message.author.voice.channel.name,
                                      color=0x66cc66)
            except SyntaxError as e:
                cmd.log.error(f'ERROR: {e} | TRACE: {e.with_traceback}')
                embed = discord.Embed(color=0xDB0000)
                embed.add_field(name='❗ I was unable to connect.',
                                value='The most common cause is your server being too far or a poor connection.')
            await message.channel.send(None, embed=embed)
        if bot_voice:
            if bot_voice.is_playing():
                embed = discord.Embed(
                    title='⚠ Already playing in ' + cmd.bot.voice_client_in(message.guild).channel.name,
                    color=0xFF9900)
                await message.channel.send(None, embed=embed)
                return
        while cmd.music.get_queue(message.guild.id) and len(cmd.music.get_queue(message.guild.id).queue) != 0:
            item = cmd.music.get_from_queue(message.guild.id)
            if message.guild.id in cmd.music.repeaters:
                cmd.music.add_to_queue(message.guild.id, item)
            cmd.music.currents.update({message.guild.id: item})
            sound = item['sound']
            cmd.bot.loop.create_task(cmd.music.make_player(bot_voice, item))
            def_vol = cmd.music.get_volume(cmd.db, message.guild.id)
            cmd.db.add_stats('MusicCount')
            embed = discord.Embed(color=0x0099FF)
            if item['type'] == 0:
                embed.add_field(name='🎵 Now Playing', value=sound.title)
                embed.set_thumbnail(url=sound.thumb)
                embed.set_author(name=f'{item["requester"].name}#{item["requester"].discriminator}',
                                 icon_url=user_avatar(item['requester']), url=item['url'])
                embed.set_footer(text=f'Duration: {sound.duration}')
            elif item['type'] == 1:
                embed.add_field(name='🎵 Now Playing', value=sound['title'])
                embed.set_thumbnail(url=sound['artwork_url'])
                embed.set_author(name=f'{item["requester"].name}#{item["requester"].discriminator}',
                                 icon_url=user_avatar(item['requester']), url=item['url'])
            else:
                return
            await message.channel.send(None, embed=embed)
            while bot_voice.is_playing():
                await asyncio.sleep(2)
        try:
            await bot_voice.disconnect()
            del cmd.music.voices[message.guild.id]
        except:
            pass
        del cmd.music.currents[message.guild.id]
    else:
        cmd.log.warning('Play Command Ignored Due To Server Being In The Music Initialization List')
