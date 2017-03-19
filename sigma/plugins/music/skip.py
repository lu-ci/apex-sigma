import discord


async def skip(cmd, message, args):
    if message.author.voice_channel:
        queue = cmd.bot.music.get_queue(message.server.id)
        if not queue or queue.empty():
            embed = discord.Embed(color=0xFF9900, title='⚠ The Queue Is Empty or This Is The Last Song')
            await cmd.bot.send_message(message.channel, None, embed=embed)
        else:
            player = cmd.bot.music.get_player(message.server.id)
            if player:
                player.stop()
                cmd.bot.music.kill_player(message.server.id)
