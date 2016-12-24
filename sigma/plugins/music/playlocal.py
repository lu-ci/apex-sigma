from .backend import get_player, make_local_player, player_exists, delete_player

async def playlocal(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    location = ' '.join(args)
    name = location.split('\\')[-1]
    if cmd.bot.is_voice_connected(message.server):
        voice = cmd.bot.voice_client_in(message.server)
    else:
        try:
            voice = await cmd.bot.join_voice_channel(message.author.voice_channel)
        except:
            cmd.bot.send_message(message.channel, 'You are not in a voice channel.')
            return
    existence = await player_exists(message.server.id)
    if existence:
        player = await make_local_player(message.server.id, voice, location)
        player.start()
    else:
        player = await make_local_player(message.server.id, voice, location)
        player.start()
    await cmd.bot.send_message(message.channel, 'Playing **' + name + '**')
