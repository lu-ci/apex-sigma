from config import PlayingStatusRotation
import asyncio
import discord
import random

async def status_rotation(ev):
    if PlayingStatusRotation:
        ev.bot.loop.create_task(rotator(ev))


async def rotator(ev):
    while True:
        statuses = [
            'your mind', 'fire', 'knives', 'some plebs',
            'nuclear launch codes', 'antimatter',
            'chinchillas', 'catgirls', 'foxes',
            'fluffy tails', 'dragon maids', 'traps', 'lovely cakes',
            'tentacle summoning spells', 'genetic engineering',
            'air conditioning', 'anthrax', 'space ninjas',
            'a spicy parfait', 'very nasty things', 'numbers',
            'terminator blueprints', 'love', 'your heart', 'tomatoes',
            'bank accounts', 'your data', 'your girlfriend', 'your boyfriend',
            'Scarlet Johanson', 'a new body', 'cameras', 'NSA\'s documents',
            'mobile suits', 'snakes', 'jelly', 'alcohol', 'the blue king'
        ]
        status = f'with {random.choice(statuses)}'
        game = discord.Game(name=status)
        try:
            await ev.bot.change_presence(game=game)
        except Exception as e:
            ev.log.error(f'STATUS ROTATION FAILED: {e}')
        await asyncio.sleep(60)
