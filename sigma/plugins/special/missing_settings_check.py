async def missing_settings_check(ev):
    ev.log.info('Checking Missing Settings')
    for server in ev.bot.servers:
        ev.db.check_for_missing_settings(server)
    ev.log.info('Settings Check Complete')
