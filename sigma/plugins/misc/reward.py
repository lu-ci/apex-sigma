import random
import time

async def reward(ev, message, args):
    if message.server is None:
        return
    if message.author.bot:
        return
    current_timestamp = int(time.time())
    cooldown_finder_data = {
        'Type': 'Activity',
        'UserID': message.author.id,
        'ServerID': message.server.id,
    }
    cooldown_insert_data = {
        'Type': 'Activity',
        'UserID': message.author.id,
        'ServerID': message.server.id,
        'LastTimestamp': current_timestamp,
    }
    cooldown_data = ev.db.find('Cooldowns', cooldown_finder_data)
    n = 0
    last_use = 0
    for result in cooldown_data:
        n += 1
        try:
            last_use = result['LastTimestamp']
        except:
            last_use = 0
    if n == 0:
        off_cooldown = True
        not_in_db = True
    else:
        not_in_db = False
        if current_timestamp > last_use + 60:
            off_cooldown = True
        else:
            off_cooldown = False
    if off_cooldown:
        if not_in_db:
            ev.db.insert_one('Cooldowns', cooldown_insert_data)
        else:
            updatetarget = {"UserID": message.author.id, "ServerID": message.server.id, "Type": "Activity"}
            updatedata = {"$set": {"LastTimestamp": current_timestamp}}
            ev.db.update_one('Cooldowns', updatetarget, updatedata)
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
            'Points': 0,
            'UserName': message.author.name,
            'Avatar': message.author.avatar_url,
            'Level': 0
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
            level = int(new_pts / 1690)
            updatetarget = {"UserID": message.author.id, "ServerID": message.server.id}
            updatedata = {"$set": {
                "Points": new_pts,
                'UserName': message.author.name,
                'Avatar': message.author.avatar_url,
                'Level': level
            }}
            ev.db.update_one(collection, updatetarget, updatedata)

