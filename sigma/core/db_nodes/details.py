def update_details(db, server=None, user=None):
    if server:
        location = 'ServerList'
        exists = db[location].find_one({'ServerID': server.id})
        updatetarget = {'ServerID': user.id}
        data = {
            'ServerID': server.id,
            'Icon': server.icon_url,
            'ServerName': server.name,
            'Owner': server.owner.name,
            'OwnerID': server.owner.id
        }
    elif user:
        location = 'UserList'
        exists = db[location].find_one({'UserID': user.id})
        updatetarget = {'UserID': user.id}
        if user.avatar_url != '':
            user_ava = '.'.join(user.avatar_url.split('.')[:-1])
        else:
            user_ava = user.default_avatar_url
        data = {
            'UserID': user.id,
            'UserName': user.name,
            'Avatar': user_ava,
            'Discriminator': user.discriminator
        }
    else:
        raise TypeError
    updatedata = {'$set': data}
    if exists:
        db[location].update_one(updatetarget, updatedata)
    else:
        db[location].insert_one(data)

