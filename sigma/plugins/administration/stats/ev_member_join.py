import arrow


async def ev_member_join(ev, member):
    stat_data = {
        'event': 'member_join',
        'author': member.id,
        'guild': member.guild.id,
        'timestamp': arrow.utcnow().timestamp
    }
    ev.db.insert_one('EventStats', stat_data)
