from humanfriendly.tables import format_pretty_table as boop


async def channelinfo(cmd, message, args):
    out_list = []
    if message.channel:
        n = 0
        nsfw = False
        chan = message.channel
        nsfw_check = cmd.db.find('NSFW', {'ChannelID': chan.id})
        for result in nsfw_check:
            n += 1
            if n > 0:
                nsfw = result['Permitted']
            else:
                nsfw = False
        out_list.append(['Name', '#' + chan.name])
        out_list.append(['Channel ID', chan.id])
        out_list.append(['Created', chan.created_at])
        out_list.append(['Is Default', chan.is_default])
        out_list.append(['Is Private', chan.is_private])
        out_list.append(['Position', chan.position])
        out_list.append(['Type', chan.type])
        out_list.append(['Topic', chan.topic])
        out_list.append(['NSFW Enabled', nsfw])
        out_text = '```\n' + boop(out_list) + '\n```'
        await cmd.bot.send_message(message.channel, out_text)
