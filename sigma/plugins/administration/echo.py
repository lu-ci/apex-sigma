from config import permitted_id


async def echo(cmd, message, args):
    if message.author.id in permitted_id:
        await cmd.bot.send_message(message.channel, ' '.join(args))
    else:
        msg = 'Sorry, <@{:s}>, you do not have permission to do that...'
        await cmd.bot.send_message(message.channel, msg.format(message.author.id))
