from humanfriendly.tables import format_pretty_table as boop


async def bots(cmd, message, args):
    bot_list = []
    cols = ['Name', 'Status']
    for user in message.server.members:
        if user.bot:
            name = user.name + '#' + user.discriminator
            status = str(user.status).replace('dnd', 'do not disturb').title()
            bot_list.append([name, status])
    out = '```haskell\n' + boop(bot_list, cols) + '\n```'
    if len(bot_list) == 0:
        await cmd.bot.send_message(message.channel, 'No bots were found on this server.')
        return
    else:
        await cmd.bot.send_message(message.channel, out)
