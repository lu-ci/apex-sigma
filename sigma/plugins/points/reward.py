import random


async def reward(ev, message, args):
    if not message.author.bot:
        if message.server:
            if not cd_state:
                act_points = random.randint(20, 45)
                points = random.randint(4, 12)
                ev.db.add_points(message.server, message.author, points)
                ev.db.add_act_points(message.server, message.author, act_points)
                ev.db.set_cooldown(message.server.id, message.author.id, 'Activity')
