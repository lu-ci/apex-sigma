import datetime
import aiohttp
import discord
from config import WarGamingAppID


async def wows(cmd, message, args):
    q = ' '.join(args).lower()
    game_region, game_username = q.split(maxsplit=1)
    if game_region == 'na':
        game_region = 'com'
    try:
        url_base = 'https://api.worldofwarships.' + game_region + '/wows/account/list/?application_id=' + WarGamingAppID + '&search=' + game_username
        async with aiohttp.ClientSession() as session:
            async with session.get(url_base) as data:
                initial_data = await data.json()
    except:
        await message.channel.send('`' + game_region + '` is not a valid region.')
        return
    try:
        if initial_data['status'].lower() == 'ok':
            pass
        else:
            return
    except Exception as e:
        cmd.log.error(e)
        return
    try:
        game_nickname = initial_data['data'][0]['nickname']
    except:
        await message.channel.send('User `' + game_username + '` not found.')
        return
    account_id = initial_data['data'][0]['account_id']
    url_second = 'https://api.worldofwarships.' + game_region + '/wows/account/info/?application_id=' + WarGamingAppID + '&account_id=' + str(
        account_id)
    async with aiohttp.ClientSession() as session:
        async with session.get(url_second) as data:
            main_data = await data.json()
    try:
        if main_data['status'].lower() == 'ok':
            pass
        else:
            return
    except Exception as e:
        cmd.log.error(e)
        return
    data = main_data['data'][str(account_id)]
    last_battle = data['last_battle_time']
    last_battle_conv = datetime.datetime.fromtimestamp(last_battle).strftime('%B %d, %Y %H:%M')
    leveling_tier = data['leveling_tier']
    join_date = data['created_at']
    join_date_conv = datetime.datetime.fromtimestamp(join_date).strftime('%B %d, %Y %H:%M')

    stats = data['statistics']
    distance = stats['distance']
    battle_count = stats['battles']

    pvp_stats = stats['pvp']
    max_xp = pvp_stats['max_xp']
    max_spotted_dmg = pvp_stats['max_damage_scouting']

    main_battery = pvp_stats['main_battery']
    max_frags = main_battery['max_frags_battle']
    frags = main_battery['frags']
    hits = main_battery['hits']
    max_frags_ship_id = main_battery['max_frags_ship_id']
    shots = main_battery['shots']

    max_frags_ship_url = 'https://api.worldofwarships.' + game_region + '/wows/encyclopedia/ships/?application_id=' + WarGamingAppID + '&ship_id=' + str(
        max_frags_ship_id)
    async with aiohttp.ClientSession() as session:
        async with session.get(max_frags_ship_url) as data:
            max_frags_ship_data = await data.json()

    if max_frags_ship_id is not None:
        max_frags_ship_name = max_frags_ship_data['data'][str(max_frags_ship_id)]['name']
        max_frags_ship_tier = max_frags_ship_data['data'][str(max_frags_ship_id)]['tier']
    else:
        max_frags_ship_name = 'None'
        max_frags_ship_tier = '0'

    # Divider for clarity

    embed = discord.Embed(color=0x1abc9c)
    embed.add_field(name='Nickname', value='```python\n' + game_nickname + '\n```')
    embed.add_field(name='Level', value='```python\n' + str(leveling_tier) + '\n```')
    embed.add_field(name='Join Date', value='```python\n' + join_date_conv + '\n```', inline=False)
    embed.add_field(name='Distance', value='```python\n' + str(distance) + ' KM' + '\n```')
    embed.add_field(name='Battles', value='```python\n' + str(battle_count) + '\n```')
    embed.add_field(name='Max XP From a Battle', value='```python\n' + str(max_xp) + '\n```')
    embed.add_field(name='Max Spotted Damange', value='```python\n' + str(max_spotted_dmg) + '\n```')
    embed.add_field(name='Max Kills In a Battle', value='```python\n' + str(max_frags) + '\n```')
    embed.add_field(name='Total Kills', value='```python\n' + str(frags) + '\n```')
    embed.add_field(name='Ship With Most Kills',
                    value='```python\n' + max_frags_ship_name + ' (Tier ' + str(max_frags_ship_tier) + ')' + '\n```')
    embed.add_field(name='Total Shots', value='```python\n' + str(shots) + '\n```')
    embed.add_field(name='Total Hits', value='```python\n' + str(hits) + '\n```')
    embed.add_field(name='Last Battle', value='```python\n' + last_battle_conv + '\n```')

    # Divider for clarity

    await message.channel.send(None, embed=embed)
