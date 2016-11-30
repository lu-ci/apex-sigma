from config import permitted_id


async def kill(cmd, message, args):
    if message.author.id in permitted_id:
        await cmd.bot.send_message(message.channel, 'Sigma shutting down.')
        await cmd.bot.logout()
        cmd.log.info('Terminated by user {:s}'.format(message.author.name))
        exit('Terminated by command.')
