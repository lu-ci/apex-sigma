def point_manipulation(db, server, user, points, point_type, add):
    collection = 'PointSystem'
    finddata = {
        'UserID': user.id,
        'ServerID': server.id
    }
    insert_data = {
        'UserID': user.id,
        'ServerID': server.id,
        'Points': 0,
        'XP': 0,
        'Level': 0
    }
    updatetarget = {"UserID": user.id, "ServerID": server.id}
    search_res = db[collection].find_one(finddata)
    # Check Existence
    if not search_res:
        db[collection].insert_one(insert_data)
    else:
        for key in insert_data:
            if key not in search_res:
                db[collection].update_one(updatetarget, {'$set': {key: insert_data[key]}})
            else:
                pass
    data = db[collection].find_one(finddata)
    old = data[point_type]
    if add:
        new = old + points
    else:
        new = old - points
    db[collection].update_one(updatetarget, {'$set': {point_type: new}})


def point_grabber(db, server, user, point_type):
    collection = 'PointSystem'
    finddata = {
        'UserID': user.id,
        'ServerID': server.id
    }
    insert_data = {
        'UserID': user.id,
        'ServerID': server.id,
        'Points': 0,
        'XP': 0,
        'Level': 0
    }
    search_res = db[collection].find_one(finddata)
    # Check Existence
    if not search_res:
        return insert_data[point_type]
    else:
        return search_res[point_type]
