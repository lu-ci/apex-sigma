collection = 'Inventory'


def get_inventory(db, user):
    inventory = db[collection].find_one({'UserID': user.id})
    if not inventory:
        db[collection].insert_one({'UserID': user.id, 'Items': []})
        inventory = []
    else:
        inventory = inventory['Items']
    return inventory


def update_inv(db, user, inv):
    db[collection].update_one(
        {'UserID': user.id},
        {
            '$set': {'Items': inv}
        }
    )


def add_to_inventory(db, user, item_data):
    inv = get_inventory(db, user)
    inv.append(item_data)
    update_inv(db, user, inv)


def del_from_inventory(db, user, item_id):
    inv = get_inventory(db, user)
    for item in inv:
        if item['ItemID'] == item_id:
            inv.remove(item)
    update_inv(db, user, inv)
