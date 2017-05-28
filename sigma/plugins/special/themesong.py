import discord


async def themesong(ev, member, before, after):
    if member.id == 293163864911249410:
        if member.voice:
            if member.voice.channel.id == 306959773314842624:
                await member.voice.channel.connect()
                bot_voice = None
                for voice_instance in ev.bot.voice_clients:
                    if voice_instance.guild.id == member.guild.id:
                        bot_voice = voice_instance
                if bot_voice:
                    source = discord.FFmpegPCMAudio(ev.resource('anthem.mp3'), executable='ffmpeg')
                    source = discord.PCMVolumeTransformer(source, volume=1.0)
                    bot_voice.play(source)
