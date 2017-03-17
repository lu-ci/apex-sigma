from sigma.core.utils import user_avatar


async def refactor_users_node(db, usrgen):
    db['UserList'].drop()
    for user in usrgen:
        user_ava = user_avatar(user)
        data = {
            'UserID': user.id,
            'UserName': user.name,
            'Avatar': user_ava,
            'Discriminator': user.discriminator
        }
        db['UserList'].insert_one(data)


async def refactor_servers_node(db, servers):
    db['ServerList'].drop()
    for server in servers:
        owner = server.owner
        if owner:
            owner_name = owner.name
            owner_id = owner.id
        else:
            owner_name = 'None'
            owner_id = 'Unknown'
        data = {
            'ServerID': server.id,
            'Icon': server.icon_url,
            'ServerName': server.name,
            'Owner': owner_name,
            'OwnerID': owner_id
        }
        db['ServerList'].insert_one(data)
