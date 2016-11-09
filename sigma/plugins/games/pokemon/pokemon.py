import requests


async def pokemon(cmd, message, args):
    poke_input = ' '.join(args)

    pokemon_url = ('http://pokeapi.co/api/v2/pokemon/' + poke_input.lower() + '/')
    poke = requests.get(pokemon_url).json()

    try:
        poke_id = str(poke['id'])
        name = str(poke['name']).title()
        number = '#' + str(poke['order'])
        height = str(poke['height'] / 10) + 'm'
        weight = str(poke['weight'] / 10) + 'kg'

        try:
            ability_1 = str(poke['abilities'][0]['ability']['name']).title()
            abil_1_vis = poke['abilities'][0]['is_hidden']
        except:
            ability_1 = str('None')
            abil_1_vis = False

        if abil_1_vis:
            a1v = 'Hidden'
        else:
            a1v = 'Not Hidden'

        try:
            abil_2_vis = poke['abilities'][1]['is_hidden']
        except:
            abil_2_vis = False

        if abil_2_vis:
            a2v = 'Hidden'
        else:
            a2v = 'Not Hidden'

        try:
            ability_2 = str(poke['abilities'][1]['ability']['name']).title()
        except:
            ability_2 = str('None')

        try:
            type_1 = str(poke['types'][0]['type']['name']).title()
        except:
            type_1 = str('None')

        # Icons
        if type_1 == 'Fire':
            icon_1 = ':fire:'
        elif type_1 == 'Fighting':
            icon_1 = ':muscle:'
        elif type_1 == 'Water':
            icon_1 = ':ocean:'
        elif type_1 == 'Flying':
            icon_1 = ':bird:'
        elif type_1 == 'Grass':
            icon_1 = ':herb:'
        elif type_1 == 'Poison':
            icon_1 = ':skull_crossbones:'
        elif type_1 == 'Electric':
            icon_1 = ':zap:'
        elif type_1 == 'Ground':
            icon_1 = ':chestnut:'
        elif type_1 == 'Psychic':
            icon_1 = ':eye:'
        elif type_1 == 'Rock':
            icon_1 = ':moyai:'
        elif type_1 == 'Ice':
            icon_1 = ':snowflake:'
        elif type_1 == 'Bug':
            icon_1 = ':bug:'
        elif type_1 == 'Dragon':
            icon_1 = ':dragon:'
        elif type_1 == 'Ghost':
            icon_1 = ':ghost:'
        elif type_1 == 'Dark':
            icon_1 = ':dark_sunglasses:'
        elif type_1 == 'Steel':
            icon_1 = ':nut_and_bolt:'
        elif type_1 == 'Fairy':
            icon_1 = ':gift_heart:'
        elif type_1 == 'None':
            icon_1 = 'None'
        else:
            icon_1 = ':necktie:'

        try:
            type_2 = str(poke['types'][1]['type']['name']).title()
        except:
            type_2 = str('None')

        if type_2 == 'Fire':
            icon_2 = ':fire:'
        elif type_2 == 'Fighting':
            icon_2 = ':muscle:'
        elif type_2 == 'Water':
            icon_2 = ':ocean:'
        elif type_2 == 'Flying':
            icon_2 = ':bird:'
        elif type_2 == 'Grass':
            icon_2 = ':herb:'
        elif type_2 == 'Poison':
            icon_2 = ':skull_crossbones:'
        elif type_2 == 'Electric':
            icon_2 = ':zap:'
        elif type_2 == 'Ground':
            icon_2 = ':chestnut:'
        elif type_2 == 'Psychic':
            icon_2 = ':eye:'
        elif type_2 == 'Rock':
            icon_2 = ':moyai:'
        elif type_2 == 'Ice':
            icon_2 = ':snowflake:'
        elif type_2 == 'Bug':
            icon_2 = ':bug:'
        elif type_2 == 'Dragon':
            icon_2 = ':dragon:'
        elif type_2 == 'Ghost':
            icon_2 = ':ghost:'
        elif type_2 == 'Dark':
            icon_2 = ':dark_sunglasses:'
        elif type_2 == 'Steel':
            icon_2 = ':nut_and_bolt:'
        elif type_2 == 'Fairy':
            icon_2 = ':gift_heart:'
        elif type_2 == 'None':
            icon_2 = 'None'
        else:
            icon_2 = ':necktie:'

        message_text = (' Name: `' + name + '` `' + number + '`\n' +
                        'ID: `' + poke_id + '`' +
                        '\nDetails:' +
                        '\nHeight: ' + height +
                        '\nWeight: ' + weight +
                        '\nType: ' + type_1 + '/' + type_2 + ' (' + icon_1 + '/' + icon_2 + ')' +
                        '\nAbilities: ' + ability_1 + ' (' + a1v + ') | ' + ability_2 + ' (' + a2v + ')\nImage: https://randompokemon.com/sprites/animated/' + poke_id + '.gif')
        await cmd.bot.send_message(message.channel, message_text)
    except:
        try:
            await cmd.bot.send_message(message.channel, str(poke['detail']))
        except:
            await cmd.bot.send_message(message.channel, 'Something went wrong')
