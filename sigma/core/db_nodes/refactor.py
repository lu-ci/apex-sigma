import asyncio
import arrow
from sigma.core.utils import user_avatar

async def refactor_users_node(db, usrgen):
    usrs = list(usrgen)
    db['UserList'].drop()
    db.log.info('UserList Dropped And Starting Refactoring Process...')
    start_time = arrow.utcnow().timestamp
    usercount = 0
    for user in usrs:
        usercount += 1
        user_ava = user_avatar(user)
        data = {
            'UserID': user.id,
            'UserName': user.name,
            'Avatar': user_ava,
            'Discriminator': user.discriminator
        }
        db['UserList'].insert_one(data)
        await asyncio.sleep(0.001)
    elapsed_time = arrow.utcnow().timestamp - start_time
    db.log.info(f'{usercount} Users Updated in {elapsed_time} seconds.')


async def refactor_servers_node(db, servers):
    srvs = servers
    db['ServerList'].drop()
    db.log.info('ServerList Dropped And Starting Refactoring Process...')
    start_time = arrow.utcnow().timestamp
    for server in srvs:
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
        await asyncio.sleep(0.001)
    elapsed_time = arrow.utcnow().timestamp - start_time
    db.log.info(f'{len(servers)} Servers Updated in {elapsed_time} seconds.')
