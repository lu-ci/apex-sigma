import os
import yaml
import arrow
import random
import hashlib

rarity_translation = {
    0: 'trash',
    1: 'common',
    2: 'uncommon',
    3: 'rare',
    4: 'legendary',
    5: 'prime',
    6: 'spectral',
    7: 'ethereal',
    8: 'antimatter',
    9: 'omnipotent'
}

item_icons = {
    'fish': {
        'trash': '🗑',
        'common': '🦐',
        'uncommon': '🐟',
        'rare': '🐡',
        'legendary': '🦑',
        'prime': '🐠',
        'spectral': '👻',
        'ethereal': '🏵',
        'antimatter': '✴',
        'omnipotent': '🔰'
    }
}

item_colors = {
    'fish': {
        'trash': 0x696969,
        'common': 0xc16a4f,
        'uncommon': 0x55acee,
        'rare': 0xd99e82,
        'legendary': 0xf4abba,
        'prime': 0xffcc4d,
        'spectral': 0xe1e8ed,
        'ethereal': 0x553788,
        'antimatter': 0x292f33,
        'omnipotent': 0x47ded4
    }
}


def make_item_id(message):
    composition = f'{message.author.id}_{message.id}_{arrow.utcnow().timestamp}'
    crypt = hashlib.new('md5')
    crypt.update(composition.encode('utf-8'))
    return crypt.hexdigest()


def get_item_settings(item_type):
    class ItemOptions(object):
        colors = item_colors[item_type]
        icons = item_icons[item_type]

    return ItemOptions


def make_item_class(item_data, settings):
    class SigmaItem(object):
        name = item_data['name']
        description = item_data['description']
        rarity = item_data['rarity']
        rarity_name = rarity_translation[rarity]
        item_type = item_data['type']
        value = item_data['value']
        icon = settings.icons[rarity_name]
        color = settings.colors[rarity_name]
        item_file_id = item_data['item_file_id']
    return SigmaItem


def get_all_items(item_type, location_base):
    settings = get_item_settings(item_type)
    output = {}
    fish_file_list = os.listdir(f'{location_base}/{item_type.lower()}')
    for file in fish_file_list:
        if file.endswith('.yml'):
            with open(f'{location_base}/{item_type.lower()}/{file}') as item_file:
                item_id = file.split('.')[0]
                item_data = yaml.safe_load(item_file)
                item_data.update({'item_file_id': item_id})
                item_object = make_item_class(item_data, settings)
                output.update({item_id: item_object})
    return output


def get_items_in_rarity(item_dict, rarity):
    output = []
    for item_key in item_dict:
        if item_dict[item_key].rarity == rarity:
            output.append(item_dict[item_key])
    return output


def roll_rarity():
    rarities = {
        0: 0,
        1: 4000,
        2: 7000,
        3: 9000,
        4: 9500,
        5: 9800,
        6: 9910,
        7: 9960,
        8: 9985,
        9: 9995
    }
    roll = random.randint(1, 10000)
    print(roll)
    lowest = 0
    for rarity in rarities:
        if rarities[rarity] <= roll:
            lowest = rarity
        else:
            break
    return lowest
