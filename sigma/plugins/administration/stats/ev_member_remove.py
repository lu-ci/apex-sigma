async def ev_member_remove(ev, member):
    def_stat_data = {
        'event': 'member_remove',
        'count': 0
    }
    collection = 'EventStats'
    check = ev.db.find_one(collection, {"event": 'member_remove'})
    if not check:
        ev.db.insert_one(collection, def_stat_data)
        ev_count = 0
    else:
        ev_count = check['count']
    ev_count += 1
    updatetarget = {"event": 'member_remove'}
    updatedata = {"$set": {'count': ev_count}}
    ev.db.update_one(collection, updatetarget, updatedata)
