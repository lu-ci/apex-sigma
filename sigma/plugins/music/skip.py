import discord


async def skip(cmd, message, args):
    if message.author.voice:
        queue = cmd.bot.music.get_queue(message.guild.id)
        if not queue or queue.empty():
            embed = discord.Embed(color=0xFF9900, title='⚠ The Queue Is Empty or This Is The Last Song')
            await message.channel.send(None, embed=embed)
        else:
            if message.guild.voice_client:
                voice = message.guild.voice_client
                voice.stop()
