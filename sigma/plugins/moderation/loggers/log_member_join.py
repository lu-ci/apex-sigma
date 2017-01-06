async def log_member_join(ev, member):
    try:
        loggin_active = ev.db.get_settings(member.server.id, 'LoggingEnabled')
    except KeyError:
        ev.db.set_settings(member.server.id, 'LoggingEnabled', False)
        loggin_active = False
    if loggin_active:
        ev.db.log_join(member)
