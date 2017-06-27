import asyncio


async def population_clockwork(ev):
    search = ev.db.find_one('GeneralStats', {'name': 'population'})
    if not search:
        ev.db.insert_one('GeneralStats', {'name': 'population'})
    ev.bot.loop.create_task(update_population_stats_node(ev))


async def update_population_stats_node(ev):
    while True:
        collection = 'GeneralStats'
        server_count = len(list(ev.bot.guilds))
        member_count = len(list(ev.bot.get_all_members()))
        channel_count = len(list(ev.bot.get_all_channels()))
        # Guilds
        updatetarget = {"name": 'population'}
        updatedata = {"$set": {'guild_count': server_count}}
        ev.db.update_one(collection, updatetarget, updatedata)
        # Members
        updatetarget = {"name": 'population'}
        updatedata = {"$set": {'member_count': member_count}}
        ev.db.update_one(collection, updatetarget, updatedata)
        # Channels
        updatetarget = {"name": 'population'}
        updatedata = {"$set": {'channel_count': channel_count}}
        ev.db.update_one(collection, updatetarget, updatedata)
        await asyncio.sleep(60)
