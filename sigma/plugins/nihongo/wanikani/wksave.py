from sigma.core.database import IntegrityError


async def wksave(cmd, message, args):
    coll = 'WaniKani'
    try:
        await cmd.delete_call_message()
    except Exception as e:
        cmd.log.error(e)
        cmd.log.info('Message in private channel, unable to delete...')

    user_id = int(message.author.id)

    try:
        mode = args.pop(0)
        payload = ' '.join(args)

        if not mode:
            await cmd.reply('Bind your Discord profile and your API key or username\n'
                            'Usage: `{0:s}wksave' + ' key <your api key here>` or `{0:s}wksave' + ' username <your username here>`'.format(
                cmd.prefix))
            return
        if mode not in ['key', 'username', 'remove']:  # remove
            await cmd.reply('Unknown argument')
            return
        if mode == 'key':
            if len(payload) < 32 or len(payload) > 32:
                await cmd.reply('The Key Seems Invalid...')
                return

        if mode == 'remove':  # remove
            query = {'UserID': user_id}
            cmd.db.delete_one(coll, query)

            await cmd.reply('Record deleted')
            return

        if mode == 'key':
            insert_query = {
                'UserID': user_id,
                'WKAPIKey': payload,
                'WKUsername': None
            }
            update_query = {'$set': {
                'WKAPIKey': payload,
                'WKUsername': None
            }}
        elif mode == 'username':
            insert_query = {
                'UserID': user_id,
                'WKAPIKey': None,
                'WKUsername': payload
            }
            update_query = {'$set': {
                'WKAPIKey': None,
                'WKUsername': payload
            }}
        else:
            return

        n = 0
        check_exist_qry = {'UserID': user_id}
        find_res = cmd.db.find(coll, check_exist_qry)
        for result in find_res:
            n += 1
        if n == 0:
            cmd.db.insert_one(coll, insert_query)
            await cmd.reply(mode.capitalize() + ' Safely Stored. :key:')
        else:
            update_target = {'UserID': user_id}
            cmd.db.update_one(coll, update_target, update_query)
            await cmd.reply(mode.capitalize() + ' Updated. :key:')

    except Exception as e:
        cmd.log.error(e)
        await cmd.reply('Error while parsing the input message')
