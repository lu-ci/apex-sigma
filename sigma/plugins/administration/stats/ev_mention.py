import arrow


async def ev_mention(ev, message, args):
    command_data = {
        'name': ev.name,
    }
    for key in ['global', 'sfw', 'admin', 'partner', 'pmable']:
        command_data[key] = ev.perm[key]
    if message.guild:
        channel_id = message.channel.id
        guild_id = message.guild.id
    else:
        channel_id = None
        guild_id = None
    stat_data = {
        'event': 'mention',
        'author': message.author.id,
        'channel': channel_id,
        'guild': guild_id,
        'timestamp': arrow.utcnow().timestamp
    }
    ev.db.insert_one('EventStats', stat_data)
