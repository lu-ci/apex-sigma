import asyncio


async def mrs(cmd, message, args):
    cmd.db.add_stats('MRSCount')
    voice = await cmd.bot.join_voice_channel(message.author.voice_channel)
    player = voice.create_ffmpeg_player(cmd.resource('mrs.wav'))
    player.start()
    while not player.is_done():
        asyncio.sleep(1)
    await voice.disconnect()
