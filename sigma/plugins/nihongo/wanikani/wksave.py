from sigma.core.database import IntegrityError
from .logger import log


async def wksave(bot, message, args):
    try:
        await bot.delete_message(message)
    except:
        log.info('Message in private channel, unable to delete...')
        pass

    try:
        await bot.type()
    except:
        pass

    user_id = str(message.author.id)

    try:
        args = message.content[len(bot.prefix) + len('wksave') + 1:]

        mode = args[:args.find(' ')].strip()
        payload = args[args.find(' ') + 1:].strip()  # key or username

        if mode == '':
            await bot.reply('Bind your Discord profile and your API key or username\n'
                    'Usage: `{0:s}wksave' + ' key <your api key here>` or `{0:s}wksave' + ' username <your username here>`'.format(bot.prefix))
            return
        if mode not in ['key', 'username', 'remov']:  # remove
            await bot.reply('Unknown argument')
            return
        if mode == 'key':
            if len(payload) < 32 or len(payload) > 32:
                await bot.reply('The Key Seems Invalid...')
                return

        if mode == 'remov':  # remove
            query = "DELETE from WANIKANI where USER_ID=?;"
            bot.db.execute(query, user_id)
            bot.db.commit()

            await bot.reply('Record deleted')
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
                    await bot.reply('Retry {:d}/{:d}'.format(i, retries))

                bot.db.execute(insert_query, user_id, payload)
                bot.db.commit()
                await bot.reply(mode.capitalize() + ' Safely Stored. :key:')
                break
            except IntegrityError:
                await bot.reply('A Key for your User ID already exists, removing...')

                bot.db.rollback()
                query = "DELETE from WANIKANI where USER_ID=?;"
                bot.db.execute(query, user_id)
                bot.db.commit()

                continue
            except UnboundLocalError as e:
                log.error(e)
                await bot.reply('There doesn\'t seem to be a key or username tied to you...\nYou can add your it by sending a direct message to me with the WKSave Command, for example:\n`{0:s}wksave' + ' 16813135183151381`\nand just replace the numbers with your WK API Key!'.format(bot.prefix))
            except Exception as e:
                log.error(e)
                await bot.reply('Something went horribly wrong!')

    except Exception as e:
        log.error(e)
        await bot.reply('Error while parsing the input message')
