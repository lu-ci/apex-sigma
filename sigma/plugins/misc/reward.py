import random


async def reward(ev, message, args):
    if message.server is None:
        return
    if message.author.bot:
        return
    target = None
    n = 0
    collection = 'PointSystem'
    finddata = {
        'UserID': message.author.id,
        'ServerID': message.server.id
    }
    insertdata = {
        'UserID': message.author.id,
        'ServerID': message.server.id,
        'Points': 0
    }
    finddata_results = ev.db.find(collection, finddata)
    for item in finddata_results:
        n += 1
        target = item
    if n == 0:
        ev.db.insert_one(collection, insertdata)
    else:
        curr_pts = target['Points']
        add_pts = random.randint(5, 20)
        new_pts = curr_pts + add_pts
        updatetarget = {"UserID": message.author.id, "ServerID": message.server.id}
        updatedata = {"$set": {"Points": new_pts}}
        ev.db.update_one(collection, updatetarget, updatedata)
