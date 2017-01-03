from .backend import get_player


async def stop(cmd, message, args):
    player = await get_player(message.server.id)
    if not player:
        await cmd.bot.send_message(message.channel, 'Nothing is currently playing.')
    else:
        if player.is_playing():
            player.stop()
            await cmd.bot.send_message(message.channel, 'Player stopped.')
        else:
            await cmd.bot.send_message(message.channel, 'Nothing is currently playing.')
