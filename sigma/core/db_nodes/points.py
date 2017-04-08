import arrow


def default_data(server, user, points, add):
    if add:
        total_pts = points
    else:
        total_pts = 0
    data = {
        'UserID': user.id,
        'Total': total_pts,
        'Servers': {server.id: total_pts}
    }
    return data


def point_manipulation(db, server, user, points, add):
    collection = 'PointSystem'
    data = db[collection].find_one({'UserID': user.id})
    if data:
        total_pts = data['Total']
        servers = data['Servers']
        if server.id in servers:
            if add:
                new_pts = servers[server.id] + points
                total_pts += points
            else:
                new_pts = servers[server.id] - points
        else:
            new_pts = points
        servers.update({server.id: new_pts})
        db[collection].update_one({'UserID': user.id}, {'$set': {'Servers': servers, 'Total': total_pts}})
    else:
        data = default_data(server, user, points, add)
        db[collection].insert_one(data)


def point_grabber(db, user):
    collection = 'PointSystem'
    data = db[collection].find_one({'UserID': user.id})
    return data
