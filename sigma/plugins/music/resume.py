from .backend import get_player


async def resume(cmd, message, args):
    player = await get_player(message.server.id)
    if not player:
        await cmd.bot.send_message(message.channel, 'Nothing is currently playing.')
    else:
        if not player.is_playing():
            player.resume()
            await cmd.bot.send_message(message.channel, 'Player resumed.')
        else:
            await cmd.bot.send_message(message.channel, 'The player is already currently playing.')
