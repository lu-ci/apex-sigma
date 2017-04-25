import discord


async def disconnect(cmd, message, args):
    if not message.author.voice:
        embed = discord.Embed(
            title='⚠ I don\'t see you in a voice channel', color=0xFF9900)
        await message.channel.send(None, embed=embed)
        return
    if message.guild.id in cmd.music.voices:
        voice = cmd.music.voices[message.guild.id]
        cmd.music.purge_queue(message.guild.id)
        voice.stop()
        await voice.disconnect()
        del cmd.music.voices[message.guild.id]
        embed = discord.Embed(color=0x66CC66, title=f'✅ Disconnected From {voice.channel.name}')
        embed.set_footer(text='And purged queue.')
    else:
        embed = discord.Embed(
            title='⚠ I am not in a voice channel', color=0xFF9900)
    await message.channel.send(None, embed=embed)
