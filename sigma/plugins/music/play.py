import time
import discord
import asyncio
from sigma.core.utils import user_avatar
from sigma.core.stats import add_special_stats
from .init_clock import init_clock


def get_voice_members_count(voice_channel):
    member_count = 0
    for member in voice_channel.members:
        if not member.bot:
            if not member.voice.deaf:
                if not member.voice.self_deaf:
                    member_count += 1
    return member_count


def music_is_ongoing(cmd, sid, voice_instance):
    queue_exists = cmd.music.get_queue(sid)
    gueue_empty = cmd.music.get_queue(sid).empty()
    if voice_instance:
        voice_member_count = get_voice_members_count(voice_instance.channel)
    else:
        voice_member_count = 0
    if queue_exists and gueue_empty is not True and voice_member_count != 0:
        ongoing = True
    else:
        ongoing = False
    return ongoing


async def play(cmd, message, args):
    if args:
        task = cmd.bot.plugin_manager.commands['queue'].call(message, args)
        await task
    if message.guild.id not in cmd.music.initializing:
        bot_voice = message.guild.voice_client
        if not message.author.voice:
            embed = discord.Embed(title='⚠ I don\'t see you in a voice channel', color=0xFF9900)
            await message.channel.send(None, embed=embed)
            return
        srv_queue = cmd.music.get_queue(message.guild.id)
        if srv_queue.empty():
            embed = discord.Embed(
                title='⚠ The queue is empty', color=0xFF9900)
            await message.channel.send(None, embed=embed)
            return
        cmd.music.add_init(message.guild.id)
        cmd.bot.loop.create_task(init_clock(cmd.music, message.guild.id))
        if not bot_voice:
            try:
                try:
                    can_connect = message.guild.me.permissions_in(message.author.voice.channel).connect
                    can_talk = message.guild.me.permissions_in(message.author.voice.channel).speak
                    if can_connect and can_talk:
                        bot_voice = await message.author.voice.channel.connect()
                    else:
                        embed = discord.Embed(title=f'⚠ I am not allowed to join {message.author.voice.channel.name}.',
                                              color=0xFF9900)
                        await message.channel.send(None, embed=embed)
                        return
                except discord.ClientException:
                    bot_voice = None
                    for voice_instance in cmd.bot.voice_clients:
                        if voice_instance.guild.id == message.guild.id:
                            bot_voice = voice_instance
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
                if not args:
                    embed = discord.Embed(
                        title=f'⚠ Already playing in {message.guild.get_member(cmd.bot.user.id).voice.channel.name}',
                        color=0xFF9900)
                    await message.channel.send(None, embed=embed)
                    return
        while music_is_ongoing(cmd, message.guild.id, message.guild.me.voice):
            item = await cmd.music.get_from_queue(message.guild.id)
            if message.guild.id in cmd.music.repeaters:
                await cmd.music.add_to_queue(message.guild.id, item)
            cmd.music.currents.update({message.guild.id: item})
            sound = item['sound']
            try:
                await cmd.music.make_player(bot_voice, item)
            except:
                pass
            add_special_stats(cmd.db, 'songs_played')
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
            elif item['type'] == 2:
                embed.add_field(name='🎵 Now Playing', value=f"{sound['artist']} - {sound['title']}")
                embed.set_thumbnail(url=sound['thumbnail'])
                embed.set_author(name=f'{item["requester"].name}#{item["requester"].discriminator}',
                                 icon_url=user_avatar(item['requester']), url=item['url'])
                duration = f'Duration: {time.strftime("%H:%M:%S", time.gmtime(int(item["sound"]["duration"])))}'
                embed.set_footer(text=duration)
            else:
                return
            await message.channel.send(None, embed=embed)
            while bot_voice.is_playing():
                await asyncio.sleep(2)
        try:
            await bot_voice.disconnect()
        except:
            pass
        try:
            del cmd.music.currents[message.guild.id]
        except:
            pass
    else:
        cmd.log.warning('Play Command Ignored Due To Server Being In The Music Initialization List')
