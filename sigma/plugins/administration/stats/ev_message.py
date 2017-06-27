async def ev_message(ev, message, args):
    def_stat_data = {
        'event': 'message',
        'count': 0
    }
    collection = 'EventStats'
    check = ev.db.find_one(collection, {"event": 'message'})
    if not check:
        ev.db.insert_one(collection, def_stat_data)
        ev_count = 0
    else:
        ev_count = check['count']
    ev_count += 1
    updatetarget = {"event": 'message'}
    updatedata = {"$set": {'count': ev_count}}
    ev.db.update_one(collection, updatetarget, updatedata)
