import aiohttp
import discord
import datetime
from config import ParagonAPIKey


async def paragon(cmd, message, args):
    if args:
        username = ' '.join(args)
        search_url = f'https://developer-paragon.epicgames.com/v1/accounts/find/{username.replace(" ", "%20")}'
        headers = {'X-Epic-ApiKey': ParagonAPIKey, 'Accept': 'application/json; charset=utf-8'}
        pgn_icon = 'https://cdn1.unrealengine.com/2957004/favicons/favicon-32x32-121c1fa91b8c69fc4b41a084af1f1e26.png'
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url, headers=headers) as data:
                search_response = await data.json()
        try:
            account_id = search_response['accountId']
            stats_url = f'https://developer-paragon.epicgames.com/v1/account/{account_id}'
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{stats_url}/stats', headers=headers) as data:
                    stats_data = await data.json()
                async with session.get(f'{stats_url}', headers=headers) as data:
                    profile_data = await data.json()
            stats = stats_data['total']
            try:
                core_kills = stats['kills_core']
            except:
                core_kills = None
            response = discord.Embed(color=0xEEEEEE)
            response.set_author(name=f'{profile_data["displayName"]} | Level {stats["account_level_up"]}',
                                icon_url=pgn_icon)
            response.add_field(name='Reputation', value=stats['rep'])
            response.add_field(name='Time Played', value=str(datetime.timedelta(seconds=stats['time_played'])))
            response.add_field(name='Experience', value=stats['xp'])
            response.add_field(name='Games Played', value=stats['games_played'])
            response.add_field(name='Games Won', value=stats['games_won'])
            response.add_field(name='Games Left', value=stats['games_left'])
            response.add_field(name='Hero Kills', value=stats['kills_hero'])
            response.add_field(name='Core Kills', value=core_kills)
            response.add_field(name='Minion Kills', value=stats['kills_minions'])

        except Exception:
            response = discord.Embed(color=0xDB0000, title=f'❗ User {username} Not Found')
        await message.channel.send(None, embed=response)
