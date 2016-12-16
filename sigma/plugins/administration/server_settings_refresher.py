import time


async def server_settings_refresher(ev, message, args):
    find_res = ev.db.find('Cooldowns', {'Type': 'ServerSettingsUpdater'})
    cd = 0
    n = 0
    for res in find_res:
        n += 1
        try:
            cd = res['LastTimestamp']
        except:
            cd = 0
    timestamp = int(time.time())
    if n == 0:
        on_cd = False
        data = {'Type': 'ServerSettingsUpdater',
                'LastTimestamp': timestamp
                }
        ev.db.insert_one('Cooldowns', data)
    else:
        if (cd + 180) < timestamp:
            on_cd = False
            updatetarget = {
                'Type': 'ServerSettingsUpdater'}
            updatedata = {"$set": {'LastTimestamp': timestamp}}
            ev.db.update_one('Cooldowns',updatetarget, updatedata)
        else:
            on_cd = True
    if not on_cd:
        servers = []
        for srv in ev.bot.servers:
            servers.append(srv)
        ev.db.init_server_settings(servers)
