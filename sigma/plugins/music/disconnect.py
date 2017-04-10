import discord


async def disconnect(cmd, message, args):
    if not message.author.voice_channel:
        embed = discord.Embed(
            title='⚠ I don\'t see you in a voice channel', color=0xFF9900)
        await message.channel.send(None, embed=embed)
        return
    voice = cmd.bot.voice_client_in(message.server)
    if voice:
        cmd.music.purge_queue(message.server.id)
        await voice.disconnect()
        embed = discord.Embed(color=0x66CC66, title=f'✅ Disconnected From {voice.channel.name}')
        embed.set_footer(text='And purged queue.')
    else:
        embed = discord.Embed(
            title='⚠ I am not in a voice channel', color=0xFF9900)
    await message.channel.send(None, embed=embed)
