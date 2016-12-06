import time


async def servers_updater(ev, message, args):
    find_res = ev.db.find('Cooldowns', {'Type': 'ServerUpdater'})
    n = 0
    cd = 0
    for res in find_res:
        n += 1
        try:
            cd = res['LastTimestamp']
        except:
            cd = 0
    timestamp = int(time.time())
    if n == 0:
        on_cd = False
        data = {'Type': 'ServerUpdater',
                'LastTimestamp': timestamp
                }
        ev.db.insert_one('Cooldowns', data)
    else:
        if (cd + 180) < timestamp:
            on_cd = False
            updatetarget = {
                'Type': 'ServerUpdater'}
            updatedata = {"$set": {'LastTimestamp': timestamp}}
            ev.db.update_one('Cooldowns',updatetarget, updatedata)
        else:
            on_cd = True
    if not on_cd:
        for server in ev.bot.servers:
            member_count = 0
            bot_count = 0
            srch_data = {
                'ServerID': server.id
            }
            serv_found = 0
            search = ev.db.find('Servers', srch_data)
            for res in search:
                serv_found += 1
            for member in server.members:
                if member.bot:
                    bot_count += 1
                else:
                    member_count += 1
            if serv_found == 0:
                data = {
                    'ServerID': server.id,
                    'ServerName': server.name,
                    'ServerAvatar': server.icon_url,
                    'Created': server.created_at,
                    'DefaultChannelID': server.default_channel.id,
                    'DefaultChannelName': server.default_channel.name,
                    'MemberCount': member_count,
                    'BotCount': bot_count,
                    'Owner': server.owner.name,
                    'OwnerID': server.owner_id,
                    'Region': str(server.region),
                    'SecLevel': str(server.verification_level),
                    'MFALevel': str(server.mfa_level)
                }
                ev.db.insert_one('Servers', data)
            else:
                updatedata = {
                    'ServerName': server.name,
                    'ServerAvatar': server.icon_url,
                    'DefaultChannelID': server.default_channel.id,
                    'DefaultChannelName': server.default_channel.name,
                    'MemberCount': member_count,
                    'BotCount': bot_count,
                    'Owner': server.owner.name,
                    'OwnerID': server.owner_id,
                    'Region': str(server.region),
                    'SecLevel': str(server.verification_level),
                    'MFALevel': str(server.mfa_level)
                }
                updatetarget = {"ServerID": server.id}
                updatedata = {"$set": updatedata}
                ev.db.update_one('Servers', updatetarget, updatedata)
        serv_count = 0
        user_count = 0
        for server in ev.bot.servers:
            serv_count += 1
            for user in server.members:
                user_count += 1
        check_res = ev.db.find('Stats', {'Role': 'Stats'})
        n = 0
        for res in check_res:
            n += 1
        if n == 0:
            stats_data_full = {
                'Role': 'Stats',
                'ServerCount': serv_count,
                'UserCount': user_count,
            }
            ev.db.insert_one('Stats', stats_data_full)
        else:
            stats_data_update = {
                'ServerCount': serv_count,
                'UserCount': user_count,
            }
            updatetarget = {"Role": 'Stats'}
            updatedata = {"$set": stats_data_update}
            ev.db.update_one('Stats', updatetarget, updatedata)
    else:
        return
