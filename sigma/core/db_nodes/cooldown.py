import arrow


def set_cooldown_node(db, sid, uid, command):
    timestamp = arrow.utcnow().timestamp
    collection = 'Cooldowns'
    find_data = {
        'ServerID': sid,
        'UserID': uid,
        'Type': command
    }
    find_results = db[collection].find(find_data)
    n = len(list(find_results))
    if n == 0:
        data = {
            'ServerID': sid,
            'UserID': uid,
            'Type': command,
            'LastTimestamp': timestamp
        }
        db[collection].insert_one(data)
    else:
        updatetarget = {
            'ServerID': sid,
            'UserID': uid,
            'Type': command}
        updatedata = {"$set": {'LastTimestamp': timestamp}}
        db[collection].update_one(updatetarget, updatedata)


def on_cooldown_node(db, sid, uid, command, cooldown):
    collection = 'Cooldowns'
    find_data = {
        'ServerID': sid,
        'UserID': uid,
        'Type': command
    }
    find_results = db[collection].find(find_data)
    n = 0
    target = None
    for res in find_results:
        n += 1
        target = res
    if n == 0:
        return False
    else:
        curr_stamp = arrow.utcnow().timestamp
        last_stamp = target['LastTimestamp']
        if (last_stamp + cooldown) < curr_stamp:
            return False
        else:
            return True


def get_cooldown_node(db, sid, uid, command, cooldown):
    collection = 'Cooldowns'
    find_data = {
        'ServerID': sid,
        'UserID': uid,
        'Type': command
    }
    find_results = db[collection].find(find_data)
    n = 0
    target = None
    for res in find_results:
        n += 1
        target = res
    if n == 0:
        return 0
    else:
        curr_stamp = arrow.utcnow().timestamp
        last_stamp = target['LastTimestamp']
        cd_time = (last_stamp + cooldown) - curr_stamp
        return cd_time
