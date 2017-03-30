from config import Prefix
import asyncio
import discord
import random
import yaml
import arrow
import os


async def status_rotation(ev):
    ev.bot.loop.create_task(rotator(ev))


async def rotator(ev):
    while True:
        if os.path.exists('cache/status_rotation_clock.yml'):
            with open('cache/status_rotation_clock.yml', 'r') as clock_file:
                clock_data = yaml.safe_load(clock_file)
        else:
            clock_data = {'stamp': 0}
        last_stamp = clock_data['stamp']
        if last_stamp + 20 < arrow.utcnow().timestamp:
            with open('cache/status_rotation_clock.yml', 'w') as clock_file:
                yaml.safe_dump({'stamp': arrow.utcnow().timestamp}, clock_file)
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
                f'with {random.choice(ev.bot.donors)["name"]}',
                f'with {random.choice(funny)}',
                f'with {random.choice(ev.bot.authors)}'
            ]
            status = random.choice(statuses)
            game = discord.Game(name=status)
            try:
                await ev.bot.change_presence(game=game)
            except Exception as e:
                ev.log.error(f'STATUS ROTATION FAILED: {e}')
        await asyncio.sleep(20)
