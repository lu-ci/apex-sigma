def check_channel_nsfw(db, channel_id):
    n = 0
    item = None
    coll = 'NSFW'
    finddata = {
        'ChannelID': channel_id,
    }
    finddata_res = db.find(coll, finddata)
    for item in finddata_res:
        n += 1
    print(n)
    if n == 0:
        return False
    else:
        active = item['Permitted']
        return active


def set_channel_nsfw(db, channel_id):
    success = False
    n = 0
    item = None
    coll = 'NSFW'
    finddata = {
        'ChannelID': channel_id,
    }
    finddata_res = db.find(coll, finddata)
    for item in finddata_res:
        n += 1
    if n == 0:
        insertdata = {
            'ChannelID': channel_id,
            'Permitted': True
        }
        db.insert_one(coll, insertdata)
        success = True
    else:
        active = item['Permitted']
        updatetarget = {"ChannelID": channel_id}
        updatepermit = {"$set": {"Permitted": True}}
        updateunpermit = {"$set": {"Permitted": False}}
        if active:
            db.update_one(coll, updatetarget, updateunpermit)
        else:
            db.update_one(coll, updatetarget, updatepermit)
            success = True
    return success


def check_admin(user, channel):
    return user.permissions_in(channel).administrator


def check_ban(user, channel):
    return user.permissions_in(channel).ban_members


def check_kick(user, channel):
    return user.permissions_in(channel).kick_members


def check_man_msg(user, channel):
    return user.permissions_in(channel).manage_messages


def check_man_roles(user, channel):
    return user.permissions_in(channel).manage_roles


def check_write(user, channel):
    return user.permissions_in(channel).send_messages


def check_man_chan(user, channel):
    return user.permissions_in(channel).manage_channels
