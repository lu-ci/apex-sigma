from sigma.core.database import IntegrityError


async def wksave(cmd, message, args):
    try:
        await cmd.delete_call_message()
    except Exception as e:
        cmd.log.error(e)
        cmd.log.info('Message in private channel, unable to delete...')

    user_id = str(message.author.id)

    try:
        mode = args.pop(0)
        payload = ' '.join(args)

        if not mode:
            await cmd.reply('Bind your Discord profile and your API key or username\n'
                    'Usage: `{0:s}wksave' + ' key <your api key here>` or `{0:s}wksave' + ' username <your username here>`'.format(cmd.prefix))
            return
        if mode not in ['key', 'username', 'remov']:  # remove
            await cmd.reply('Unknown argument')
            return
        if mode == 'key':
            if len(payload) < 32 or len(payload) > 32:
                await cmd.reply('The Key Seems Invalid...')
                return

        if mode == 'remov':  # remove
            query = "DELETE from WANIKANI where USER_ID=?;"
            cmd.db.execute(query, user_id)
            cmd.db.commit()

            await cmd.reply('Record deleted')
            return

        if mode == 'key':
            insert_query = "INSERT INTO WANIKANI (USER_ID, WK_KEY) VALUES (?, ?)"
        elif mode == 'username':
            insert_query = "INSERT INTO WANIKANI (USER_ID, WK_USERNAME) VALUES (?, ?)"
        else:
            return

        retries = 3
        for i in range(0, retries + 1):
            try:
                if i:
                    await cmd.reply('Retry {:d}/{:d}'.format(i, retries))

                cmd.db.execute(insert_query, user_id, payload)
                cmd.db.commit()
                await cmd.reply(mode.capitalize() + ' Safely Stored. :key:')
                break
            except IntegrityError:
                await cmd.reply('A Key for your User ID already exists, removing...')

                cmd.db.rollback()
                query = "DELETE from WANIKANI where USER_ID=?;"
                cmd.db.execute(query, user_id)
                cmd.db.commit()

                continue
            except UnboundLocalError as e:
                cmd.log.error(e)
                await cmd.reply('There doesn\'t seem to be a key or username tied to you...\nYou can add your it by sending a direct message to me with the WKSave Command, for example:\n`{0:s}wksave' + ' 16813135183151381`\nand just replace the numbers with your WK API Key!'.format(cmd.prefix))
            except Exception as e:
                cmd.log.error(e)
                await cmd.reply('Something went horribly wrong!')

    except Exception as e:
        cmd.log.error(e)
        await cmd.reply('Error while parsing the input message')
