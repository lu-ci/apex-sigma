import asyncio
import os
import discord


async def sbo(cmd, message, args):
    cmd.db.add_stats('MRSCount')
    if not args:
        embed = discord.Embed(color=0xDB0000, title=':exclamation: No sound given.')
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    sound_name = ' '.join(args)
    if sound_name not in os.listdir(cmd.resource('sounds/')):
        embed = discord.Embed(color=0xDB0000, title=':exclamation: Sound not found.')
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    voice = await cmd.bot.join_voice_channel(message.author.voice_channel)
    player = voice.create_ffmpeg_player(cmd.resource('sounds/' + sound_name))
    player.start()
    while not player.is_done():
        asyncio.sleep(1)
    await voice.disconnect()
