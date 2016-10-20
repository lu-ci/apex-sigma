async def signup(cmd, message, args):
    query = "SELECT EXISTS (SELECT USER_ID FROM KARAOKE_LIST WHERE USER_ID=?);"
    info_grabber_checker = cmd.db.execute(query, str(message.author.id))

    for info_check in info_grabber_checker:
        if info_check[0] == 0:

            query = 'INSERT INTO KARAOKE_LIST (USER_ID, USER_NAME) VALUES (?, ?)'
            cmd.db.execute(query, str(message.author.id), str(message.author.name))
            cmd.db.commit()

            await cmd.reply('Thank you for signing up for the Karaoke event, <@' + message.author.id + '>!')
        else:
            await cmd.reply('It seems you\'ve already signed up, <@' + message.author.id + '>!')
