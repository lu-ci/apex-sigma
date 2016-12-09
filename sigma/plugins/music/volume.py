from .backend import get_player


async def volume(cmd, message, args):
    player = await get_player(message.server.id)
    if player:
        if not args:
            vol = player.volume
            await cmd.bot.send_message(message.channel, 'The player volume is **' + str(vol * 100) + '%**.')
        else:
            try:
                vol = int(args[0]) / 100
            except:
                await cmd.bot.send_message(message.channel, 'Invalid volume input.')
                return
            if 200 < int(args[0]) < 0:
                await cmd.bot.send_message(message.channel, 'Invalid volume input.')
                return
            else:
                print(vol)
                player.volume = vol
    else:
        await cmd.bot.send_message(message.channel, 'Nothing is playing at the moment.')
