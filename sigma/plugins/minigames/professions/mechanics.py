import arrow
import random
import hashlib


def make_item_id(message):
    composition = f'{message.author.id}_{message.id}_{arrow.utcnow().timestamp}'
    crypt = hashlib.new('md5')
    crypt.update(composition.encode('utf-8'))
    return crypt.hexdigest()


def roll_rarity():
    rarities = {
        'trash': {
            'low': 0,
            'high': 15
        },
        'common': {
            'low': 16,
            'high': 50
        },
        'uncommon': {
            'low': 51,
            'high': 80
        },
        'rare': {
            'low': 81,
            'high': 95
        },
        'legendary': {
            'low': 96,
            'high': 100
        }
    }
    roll = random.randint(0, 100)
    for criteria in rarities:
        if rarities[criteria]['high'] >= roll >= rarities[criteria]['low']:
            return criteria
