import aiohttp
import discord


async def pokemon(cmd, message, args):
    poke_input = ' '.join(args)

    pokemon_url = ('http://pokeapi.co/api/v2/pokemon/' + poke_input.lower())
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(pokemon_url) as data:
                poke = await data.json()
    except Exception as e:
        cmd.log.error(e)
        await message.channel.send('We had trouble communicating with the API.')
        return

    try:
        poke_id = str(poke['id'])
        name = str(poke['name']).title()
        number = str(poke['order'])
        embed = discord.Embed(color=0x1ABC9C)
        height = str(poke['height'] / 10) + 'm'
        weight = str(poke['weight'] / 10) + 'kg'
        image = 'https://randompokemon.com/sprites/animated/' + poke_id + '.gif'
        sprite = poke['sprites']['front_default']
        embed.set_author(name='#' + number + ': ' + name, icon_url=sprite, url=sprite)
        embed.set_image(url=image)
        embed.add_field(name='Measurements', value='```\nHeight: ' + height + '\nWeight: ' + weight + '\n```')
        type_text = ''
        type_urls = []
        ability_text = ''
        for ptype in poke['types']:
            type_text += '\n' + ptype['type']['name'].title()
            type_urls.append(ptype['type']['url'])
        for ability in poke['abilities']:
            if ability['is_hidden']:
                hidden = 'Hidden'
            else:
                hidden = 'Visible'
            ability_text += '\n' + ability['ability']['name'].title() + '\n - ' + hidden
        weak_against = []
        strong_against = []
        good_relations = ['no_damage_from', 'half_damage_from', 'double_damage_to']
        bad_relations = ['no_damage_to', 'half_damage_to', 'double_damage_from']
        for type_url in type_urls:
            async with aiohttp.ClientSession() as session:
                async with session.get(type_url) as data:
                    type_data = await data.json()
            dr = type_data['damage_relations']
            for relation in good_relations:
                for ptype in dr[relation]:
                    if ptype['name'].title() not in strong_against:
                        strong_against.append(ptype['name'].title())
            for relation in bad_relations:
                for ptype in dr[relation]:
                    if ptype['name'].title() not in weak_against:
                        weak_against.append(ptype['name'].title())
        embed.add_field(name='Types', value='```\n' + type_text + '\n```')
        embed.add_field(name='Abilities', value='```\n' + ability_text + '\n```')
        embed.add_field(name='Strong Against', value='```\n' + '\n'.join(strong_against) + '\n```')
        embed.add_field(name='Weak Against', value='```\n' + '\n'.join(weak_against) + '\n```')

        await message.channel.send(None, embed=embed)
    except Exception as e:
        await message.channel.send('An error has occurred.')
