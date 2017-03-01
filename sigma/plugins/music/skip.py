import discord


async def skip(cmd, message, args):
    if message.author.voice_channel:
        queue = cmd.bot.music.get_queue(message.server.id)
        if not queue or queue.empty():
            embed = discord.Embed(color=0xFF9900, title=':warning: The Queue Is Empty')
            await cmd.bot.send_message(message.channel, None, embed=embed)
        else:
            player = await cmd.bot.music.get_player(cmd, message, data=None)
            if player:
                player.stop()
                cmd.bot.music.kill_player(message.server.id)
