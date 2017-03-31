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
                'your mind', 'fire', 'knives',
                'nuclear launch codes', 'antimatter',
                'chinchillas', 'catgirls', 'foxes',
                'fluffy tails', 'dragon maids', 'traps', 'lovely cakes',
                'tentacle summoing spells', 'genetic engineering',
                'air conditioning', 'anthrax', 'space ninjas',
                'a spicy parfait', 'very nasty things', 'numbers',
                'terminator blueprints', 'love', 'your heart', 'tomatoes',
                'bank accounts', 'your data', 'your girlfriend', 'your boyfriend',
                'Scarlet Johanson', 'a new body', 'user\'s cameras'
            ]
            games = [
                'Kanon', 'Air', 'Clannad', 'Planetarian',
                'Tomoyo After', 'Little Busters!', 'Kud Wafter', 'Rewrite',
                'Angel Beats!', 'Harmonia', 'Summer Pockets', 'An Eroge', 'Nekopara',
                'Koiken Otome', 'Kono Oozora Ni Tsubasa o Hirogete', 'Grisaia no Kajitsu',
                'Fairies Story 3'
                     ]
            statuses = [
                f'{Prefix}help',
                f'with {random.choice(ev.bot.donors)["name"]}',
                f'with {random.choice(funny)}',
                f'with {random.choice(ev.bot.authors)}',
                f'{random.choice(games)}'
            ]
            status = random.choice(statuses)
            game = discord.Game(name=status)
            try:
                await ev.bot.change_presence(game=game)
            except Exception as e:
                ev.log.error(f'STATUS ROTATION FAILED: {e}')
        await asyncio.sleep(20)
