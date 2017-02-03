default_char_data = {
    'UserID': {
        'name': None,
        'level': 0,
        'class': None,
        'race': None,
        'health': 0,
        'energy': 0,
        'weapon': None,
        'armor': {
            'head': None,
            'top': None,
            'bottom': None,
            'feet': None
        },
        'currency': 0,
        'location': {
            'combat': False,
            'continent': 0,
            'region': 0,
            'x': 0,
            'y': 0,
            'dangerous': False,
            'dangerchance': 0,
            'notoriety': 0
        },
        'dead': False,
        'attack': 0,
        'defense': {
            'physical': 0,
            'magic': 0
        },
        'stats': {
            'intelligence': 0,
            'strength': 0,
            'dexterity': 0,
            'vitality': 0,
            'luck': 0,
        },
        'inventory': {
            'items': [],
            'limit': 0
        }
    }
}

weapon_example = {
    'name': None,
    'description': None,
    'item_type': 'weapon',
    'weapon_type': None,
    'requirements': {
        'intelligence': 0,
        'strength': 0,
        'dexterity': 0
    },
    'modifiers': {
        'intelligence': 0,
        'strength': 0,
        'dexterity': 0,
        'vitality': 0,
        'luck': 0,
        'physical': 0,
        'magic': 0
    }
}
