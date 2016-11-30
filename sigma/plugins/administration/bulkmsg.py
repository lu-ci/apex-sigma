from config import permitted_id


async def bulkmsg(cmd, message, args):
    input_message = ' '.join(args)

    try:
        if message.author.id in permitted_id:
            await cmd.bot.send_message(message.channel, 'Starting bulk sending... Stand by for confirmation')

            out = []
            printer = []
            no_s = 0
            no_f = 0

            for user in cmd.bot.get_all_members():
                if user.server.id == message.server.id and user.id != cmd.bot.user.id:
                    try:
                        await cmd.bot.start_private_message(user)
                        await cmd.bot.send_message(user, input_message)
                        out.append('\nSuccess: {:s}'.format(user.name))
                        no_s += 1
                    except Exception as e:
                        out.append('\nFailed: {:s}'.format(user.name))
                        printer.append('Failed: {:s}    Reason: {:s}'.format(user.name, str(e)))
                        no_f += 1

            await cmd.bot.send_message(message.channel, 'Bulk message sending complete...\n{:s}'.format(''.join(out)))

            for msg in printer:
                cmd.log.info(msg)

            cmd.log.info('Succeeded: {:d} Failed: {:d}'.format(no_s, no_f))
        else:
            await cmd.bot.send_message(message.channel, 'Not enough permissions, due to security issues, only a permitted user can use this for now...')
    except Exception as e:
        cmd.log.error(e)
