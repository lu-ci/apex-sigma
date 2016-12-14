async def server_settings_refresher(ev, message, args):
    cd_state = ev.db.on_cooldown(message.server.id, message.author.id, 'ServerSettingsUpdater', 60)
    if not cd_state:
        servers = []
        for srv in ev.bot.servers:
            servers.append(srv)
        ev.db.init_server_settings(servers)
        ev.db.set_cooldown(message.server.id, message.author.id, 'ServerSettingsUpdater')
