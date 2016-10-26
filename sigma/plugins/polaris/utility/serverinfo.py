from humanfriendly.tables import format_pretty_table as boop
async def serverinfo(cmd, message, args):
    out_list = []
    if message.server:
        serv = message.server
        out_list.append(['Name', '#' + serv.name])
        out_list.append(['Channel ID', serv.id])
        out_list.append(['Created', serv.created_at])
        out_list.append(['Default Channel', serv.default_channel])
        out_list.append(['Member Count', serv.member_count])
        out_list.append(['Owner', serv.owner])
        out_list.append(['Owner ID', serv.owner_id])
        out_list.append(['Region', serv.region])
        out_list.append(['Verification Level', serv.verification_level])
        out_list.append(['MFA Level', serv.mfa_level])
        if serv.afk_channel:
            out_list.append(['AFK Channel', serv.afk_channel])
            out_list.append(['AFK Timeout', serv.afk_timeout])
        out_text = '```\n' + boop(out_list) + '\n```'
        await cmd.reply(out_text)
