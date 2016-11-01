from humanfriendly.tables import format_pretty_table as boop
async def permissions(cmd, message, args):
    perm_list = []
    col_nam = ['Permission', 'Active']
    if args:
        user_q = message.mentions[0]
    else:
        user_q = message.author
    for permission in user_q.server_permissions:
        if permission[1] is True:
            perm_list.append(permission)
    out_text = '\n```\n' + boop(perm_list, col_nam).replace('_', ' ').title() + '\n```'
    await cmd.reply('Permissions For ' + user_q.name + out_text)
