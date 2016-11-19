async def whoplays(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    else:
        game_title = ' '.join(args)
        out_text = ''
        gamer_list = ''
        x = 0
        y = 0
        for member in message.server.members:
            if member.game:
                x += 1
                if str(member.game).lower() == game_title.lower():
                    y += 1
                    gamer_list += member.name + ', '
        gamer_list = gamer_list[:-2]
        if gamer_list == '':
            gamer_list = 'None'
        out_text += 'Out of ' + str(x) + ' people that are currently in-game, ' + str(y) + ' are playing ' + game_title + ':'
        if y == 1:
            out_text.replace('are', 'is')
        out_text += '\n```\n' + gamer_list + '\n```'
        await cmd.bot.send_message(message.channel, out_text)
