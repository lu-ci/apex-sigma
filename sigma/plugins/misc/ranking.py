async def ranking(cmd, message, args):
    await cmd.bot.send_message(message.channel,
                               'You can find the ranking for **' + message.server.name + '** here:\n<https://auroraproject.xyz/ranking?sid=' + message.server.id + '>')
