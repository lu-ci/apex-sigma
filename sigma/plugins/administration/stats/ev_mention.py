async def ev_mention(ev, message, args):
    def_stat_data = {
        'event': 'mention',
        'count': 0
    }
    collection = 'EventStats'
    check = ev.db.find_one(collection, {"event": 'mention'})
    if not check:
        ev.db.insert_one(collection, def_stat_data)
        ev_count = 0
    else:
        ev_count = check['count']
    ev_count += 1
    updatetarget = {"event": 'mention'}
    updatedata = {"$set": {'count': ev_count}}
    ev.db.update_one(collection, updatetarget, updatedata)
