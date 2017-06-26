import arrow


async def ev_member_remove(ev, member):
    stat_data = {
        'event': 'member_remove',
        'author': member.id,
        'guild': member.guild.id,
        'timestamp': arrow.utcnow().timestamp
    }
    ev.db.insert_one('EventStats', stat_data)
