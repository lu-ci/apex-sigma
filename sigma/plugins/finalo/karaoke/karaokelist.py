async def karaokelist(cmd, message, args):
    query = 'SELECT USER_NAME FROM KARAOKE_LIST'
    username_grabber = cmd.db.execute(query)

    out_text = ''
    n = 0
    for username in username_grabber:
        n += 1
        out_text += '\n#' + str(n) + ' [ ' + str(username[0]) + ' ]'

    if out_text == '':
        await cmd.reply('Nobody signed up yet...')
    else:
        await cmd.reply(out_text)
