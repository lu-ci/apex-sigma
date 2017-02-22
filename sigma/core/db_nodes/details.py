from sigma.core.utils import user_avatar


def update_details(db, server=None, user=None):
    if server:
        location = 'ServerList'
        exists = db[location].find_one({'ServerID': server.id})
        updatetarget = {'ServerID': server.id}
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
        user_ava = user_avatar(user)
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

