import discord
from .music_controller import del_player, get_player, purge_queue


async def disconnect(cmd, message, args):
    voice_connected = cmd.bot.is_voice_connected(message.server)
    if voice_connected:
        voice_instance = cmd.bot.voice_client_in(message.server)
        vc_name = voice_instance.channel.name
        await voice_instance.disconnect()
        embed = discord.Embed(title=':white_check_mark: Disconnected from ' + vc_name, color=0x66CC66)
        purge_queue(message.server)
    else:
        embed = discord.Embed(title=':warning: I am not in a voice channel currently', color=0xFF9900)
    await cmd.bot.send_message(message.channel, None, embed=embed)
