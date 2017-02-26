from config import Prefix
import asyncio
import discord
import random


async def status_rotation(ev):
    ev.bot.loop.create_task(rotator(ev))


async def rotator(ev):
    while True:
        funny = [
            'your mind',
            'fire',
            'knives',
            'nuclear launch codes',
            'antimatter',
            'chinchillas',
            'catgirls'
        ]
        statuses = [
            f'{Prefix}help',
            f'with {len(list(ev.bot.get_all_members()))} users',
            f'with {len(ev.bot.servers)} servers',
            f'with {random.choice(ev.bot.donors)}',
            f'with {random.choice(funny)}',
            f'with {random.choice(ev.bot.authors)}'
        ]
        status = random.choice(statuses)
        game = discord.Game(name=status)
        await ev.bot.change_presence(game=game)
        await asyncio.sleep(60)
