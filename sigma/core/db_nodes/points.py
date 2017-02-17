def add_points_node(db, server, user, points):
    target = None
    n = 0
    collection = 'PointSystem'
    finddata = {
        'UserID': user.id,
        'ServerID': server.id
    }
    insertdata = {
        'UserID': user.id,
        'ServerID': server.id,
        'Points': 0,
        'Level': 0
    }
    finddata_results = db[collection].find(finddata)
    for item in finddata_results:
        n += 1
        target = item
    if n == 0:
        db[collection].insert_one(insertdata)
    else:
        curr_pts = target['Points']
        add_pts = abs(points)
        new_pts = curr_pts + add_pts
        updatetarget = {"UserID": user.id, "ServerID": server.id}
        updatedata = {"$set": {
            "Points": new_pts,
        }}
        db[collection].update_one(updatetarget, updatedata)


def take_points_node(db, server, user, points):
    target = None
    n = 0
    collection = 'PointSystem'
    finddata = {
        'UserID': user.id,
        'ServerID': server.id
    }
    insertdata = {
        'UserID': user.id,
        'ServerID': server.id,
        'Points': 0,
    }
    finddata_results = db[collection].find(finddata)
    for item in finddata_results:
        n += 1
        target = item
    if n == 0:
        db[collection].insert_one(insertdata)
    else:
        curr_pts = target['Points']
        rem_pts = abs(points)
        new_pts = curr_pts - rem_pts
        updatetarget = {"UserID": user.id, "ServerID": server.id}
        updatedata = {"$set": {
            "Points": new_pts,
        }}
        db[collection].update_one(updatetarget, updatedata)


def get_points_node(db, server, user):
    target = None
    n = 0
    collection = 'PointSystem'
    finddata = {
        'UserID': user.id,
        'ServerID': server.id
    }
    search = db[collection].find(finddata)
    for res in search:
        n += 1
        target = res
    if n == 0:
        return 0
    else:
        points = target['XP']
        return points


# Activity Points Nodes

def add_act_points_node(db, server, user, points):
    target = None
    n = 0
    collection = 'PointSystem'
    finddata = {
        'UserID': user.id,
        'ServerID': server.id
    }
    insertdata = {
        'UserID': user.id,
        'ServerID': server.id,
        'XP': 0,
        'Level': 0
    }
    finddata_results = db[collection].find(finddata)
    for item in finddata_results:
        n += 1
        target = item
    if n == 0:
        db[collection].insert_one(insertdata)
    else:
        curr_pts = target['Points']
        add_pts = abs(points)
        new_pts = curr_pts + add_pts
        level = int(new_pts / 1690)
        updatetarget = {"UserID": user.id, "ServerID": server.id}
        updatedata = {"$set": {
            "XP": new_pts,
            'Level': level
        }}
        db[collection].update_one(updatetarget, updatedata)


def take_act_points_node(db, server, user, points):
    target = None
    n = 0
    collection = 'PointSystem'
    finddata = {
        'UserID': user.id,
        'ServerID': server.id
    }
    insertdata = {
        'UserID': user.id,
        'ServerID': server.id,
        'XP': 0,
        'Level': 0
    }
    finddata_results = db[collection].find(finddata)
    for item in finddata_results:
        n += 1
        target = item
    if n == 0:
        db[collection].insert_one(insertdata)
    else:
        curr_pts = target['Points']
        rem_pts = abs(points)
        new_pts = curr_pts - rem_pts
        level = int(new_pts / 1690)
        updatetarget = {"UserID": user.id, "ServerID": server.id}
        updatedata = {"$set": {
            "XP": new_pts,
            'Level': level
        }}
        db[collection].update_one(updatetarget, updatedata)


def get_act_points_node(db, server, user):
    target = None
    n = 0
    collection = 'PointSystem'
    finddata = {
        'UserID': user.id,
        'ServerID': server.id
    }
    search = db[collection].find(finddata)
    for res in search:
        n += 1
        target = res
    if n == 0:
        return 0
    else:
        points = target['Points']
        return points
