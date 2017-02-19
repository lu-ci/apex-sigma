async def missing_settings_check(ev):
    for server in ev.bot.servers:
        ev.db.check_for_missing_settings(server)
