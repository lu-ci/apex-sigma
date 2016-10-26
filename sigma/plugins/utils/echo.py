from config import permitted_id


async def echo(cmd, message, args):
    if message.author.id in permitted_id:
        await cmd.reply(' '.join(args))
    else:
        msg = 'Sorry, <@{:s}>, you do not have permission to do that...'
        await cmd.reply(msg.format(message.author.id))
