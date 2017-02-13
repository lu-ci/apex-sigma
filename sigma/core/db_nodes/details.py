def update_server_details_node(db, server):
    exists = db['ServerList'].find_one({'ServerID': server.id})
    data = {
        'ServerID': server.id,
        'Icon': server.icon_url,
        'ServerName': server.name,
        'Owner': server.owner.name,
        'OwnerID': server.owner.id
    }
    updatetarget = {'ServerID': server.id}
    updatedata = {'$set': data}
    if exists:
        db['ServerList'].update_one(updatetarget, updatedata)
    else:
        db['ServerList'].insert_one(data)


def update_user_details_node(db, user):
    exists = db['UserList'].find_one({'UserID': user.id})
    if user.avatar_url != '':
        user_ava = '.'.join(user.avatar_url.split('.')[:-1]) + '.png'
    else:
        user_ava = user.default_avatar_url
    data = {
        'UserID': user.id,
        'UserName': user.name,
        'Avatar': user_ava,
        'Discriminator': user.discriminator
    }
    updatetarget = {'User': user.id}
    updatedata = {'$set': data}
    if exists:
        db['UserList'].update_one(updatetarget, updatedata)
    else:
        db['UserList'].insert_one(data)
