import random
from config import Prefix


async def reward(ev, message, args):
    if not message.author.bot:
        if message.server:
            if not message.content.startswith(Prefix):
                if not ev.cooldown.on_cooldown(ev, message):
                    points = random.randint(3, 15)
                    ev.db.add_points(message.server, message.author, points)
                    ev.cooldown.set_cooldown(ev, message, 60)
