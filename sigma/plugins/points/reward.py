import random


async def reward(ev, message, args):
    if not message.author.bot:
        if message.server:
            if not cd_state:
                points = random.randint(4, 12)
                ev.db.add_points(message.server, message.author, points)
