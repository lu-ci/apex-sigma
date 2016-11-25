async def roles(cmd, message, args):
    n = 0
    role_list = ''
    for role in message.server.roles:
        n += 1
        role_list += role.name + ', '
    role_list = role_list[:-2].replace('@', '')
    if len(role_list) > 1800:
        role_list = role_list[:1800] + '...'
    out_text = 'There is a total of **' + str(n) + '** roles on **' + message.server.name + '**:\n'
    out_text += '```\n' + role_list + '\n```'
    await cmd.bot.send_message(message.channel, out_text)
