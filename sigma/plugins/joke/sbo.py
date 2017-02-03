import asyncio
import os
import discord


async def sbo(cmd, message, args):
    cmd.db.add_stats('MRSCount')
    if not args:
        embed = discord.Embed(color=0xDB0000, title=':exclamation: No sound given.')
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    sounds_path = ' '.join(args)
    sound_name = sounds_path.split('/')[-1]
    sounds = []
    for root, dirs, files in os.walk(cmd.resource('sounds/')):
        for file in files:
            sounds.append(file)
    if sound_name not in sounds:
        embed = discord.Embed(color=0xDB0000, title=':exclamation: Sound not found.')
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    voice = await cmd.bot.join_voice_channel(message.author.voice_channel)
    player = voice.create_ffmpeg_player(cmd.resource('sounds/' + sounds_path))
    player.start()
    while not player.is_done():
        asyncio.sleep(1)
    await voice.disconnect()
