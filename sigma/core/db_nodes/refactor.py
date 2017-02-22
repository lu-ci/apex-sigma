from sigma.core.utils import user_avatar


def refactor_users_node(db, usrgen):
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


def refactor_servers_node(db, servers):
    db['ServerList'].drop()
    for server in servers:
        data = {
            'ServerID': server.id,
            'Icon': server.icon_url,
            'ServerName': server.name,
            'Owner': server.owner.name,
            'OwnerID': server.owner.id
        }
        db['ServerList'].insert_one(data)
