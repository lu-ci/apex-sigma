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
            'low': 1,
            'high': 40
        },
        'common': {
            'low': 41,
            'high': 70
        },
        'uncommon': {
            'low': 71,
            'high': 85
        },
        'rare': {
            'low': 86,
            'high': 95
        },
        'legendary': {
            'low': 96,
            'high': 98
        },
        'prime': {
            'low': 99,
            'high': 100
        }
    }
    roll = random.randint(1, 100)
    for criteria in rarities:
        if rarities[criteria]['high'] >= roll >= rarities[criteria]['low']:
            return criteria
