import discord


async def disconnect(cmd, message, args):
    if not message.author.voice_channel:
        embed = discord.Embed(
            title=':warning: I don\'t see you in a voice channel', color=0xFF9900)
        await cmd.bot.send_message(message.channel, None, embed=embed)
        return
    await cmd.bot.disconnect()
    voice = cmd.bot.voice_client_in(message.server)
    embed = discord.Embed(color=0x66CC66, title=f':white_check_mark: Disconnected From {voice.channel.name}')
    await cmd.bot.send_message(message.channel, None, embed=embed)
