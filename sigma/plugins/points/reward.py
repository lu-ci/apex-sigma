import random


async def reward(ev, message, args):
    if message.server is None:
        return
    if message.author.bot:
        return
    cd_state = ev.db.on_cooldown(message.server.id, message.author.id, 'Activity', 60)
    if not cd_state:
        act_points = random.randint(20, 45)
        points = random.randint(4, 12)
        ev.db.add_points(message.server, message.author, points)
        ev.db.add_act_points(message.server, message.author, act_points)
        ev.db.set_cooldown(message.server.id, message.author.id, 'Activity')
