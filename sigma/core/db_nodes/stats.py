def init_stats_table_node(db):
    search = db['Stats'].find_one({'Role': 'Stats'})
    if not search:
        db['Stats'].insert_one({'Role': 'Stats'})
    else:
        return


def add_stats_node(db, statname):
    collection = 'Stats'
    find_data = {
        'Role': 'Stats'
    }
    find_res = db[collection].find_one(find_data)
    if statname in find_res:
        count = find_res[statname]
    else:
        count = 0
    new_count = count + 1
    updatetarget = {"Role": 'Stats'}
    updatedata = {"$set": {statname: new_count}}
    db[collection].update_one(updatetarget, updatedata)


def update_population_stats_node(db, servers, members):
    collection = 'Stats'
    server_count = len(list(servers))
    member_count = len(list(members))
    updatetarget = {"Role": 'Stats'}
    updatedata = {"$set": {'ServerCount': server_count}}
    db[collection].update_one(updatetarget, updatedata)
    updatetarget = {"Role": 'Stats'}
    updatedata = {"$set": {'UserCount': member_count}}
    db[collection].update_one(updatetarget, updatedata)
