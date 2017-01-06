async def log_message(ev, message, args):
    if not message.server:
        return
    try:
        loggin_active = ev.db.get_settings(message.server.id, 'LoggingEnabled')
    except KeyError:
        ev.db.set_settings(message.server.id, 'LoggingEnabled', False)
        loggin_active = False
    if loggin_active:
        ev.db.log_message(message)
