async def repertoire(cmd, message, args):
    if karaoke:
        if len(karaoke_queue) != 0:
            singer_list = ''
            n = 1
            for user in karaoke_queue:
                singer_list += '\n#' + str(n) + ': <@' + str(user.id) + '>'
                n += 1
            await cmd.reply(singer_list)
        else:
            await cmd.reply('The list seems to be empty')
    else:
        await cmd.reply('No karaoke session running')
