from steam import WebAPI
from config import SteamAPI
import discord


async def csgo(cmd, message, args):
    if not args:
        return
    csgo_input = ' '.join(args)

    try:
        api = WebAPI(SteamAPI)
        userID = api.call('ISteamUser.ResolveVanityURL', vanityurl=csgo_input, url_type=1)['response']['steamid']
        stats = api.call('ISteamUserStats.GetUserStatsForGame', steamid=userID, appid='730')['playerstats']['stats']
        summary = api.call('ISteamUser.GetPlayerSummaries', steamids=userID)['response']['players'][0]

        nickname = str(summary['personaname'])
        avatar_url = str(summary['avatarfull'])
        v = 'value'
        n = 'name'
        stat_bases = {
            "total_kills": 0,
            "total_deaths": 0,
            "total_time_played": 0,
            "total_kills_knife": 0,
            "total_kills_headshot": 0,
            "total_shots_fired": 0,
            "total_shots_hit": 0,
            "total_rounds_played": 0,
            "total_mvps": 0,
            "total_matches_won": 0,
            "total_matches_played": 0}

        for stat in stats:
            nam = stat[n]
            val = stat[v]
            if nam in stat_bases:
                stat_bases[nam] = val

        kdr = stat_bases['total_kills'] / stat_bases['total_deaths']
        accuracy = stat_bases['total_shots_hit'] / stat_bases['total_shots_fired']
        total_matches_lost = stat_bases['total_matches_played'] - stat_bases['total_matches_won']
        win_percent = stat_bases['total_matches_won'] / stat_bases['total_matches_played']

        data = {
            'Playtime': str(stat_bases['total_time_played'] // 3600) + ' Hours',
            'Kills': str(stat_bases['total_kills']),
            'Deaths': str(stat_bases['total_deaths']),
            'Kill/Death Ratio': "{0:.2f}".format(kdr),
            'Shots Fired': str(stat_bases['total_shots_fired']),
            'Shots Hit': str(stat_bases['total_shots_hit']),
            'Accuracy': "{0:.2f}".format(accuracy * 100) + '%',
            'Headshots': str(stat_bases['total_kills_headshot']),
            'Knife Kills': str(stat_bases['total_kills_knife']),
            'Rounds Played': str(stat_bases['total_rounds_played']),
            'Total MVPs': str(stat_bases['total_mvps']),
            'Matches Played': str(stat_bases['total_matches_played']),
            'Matches Won': str(stat_bases['total_matches_won']),
            'Matches Lost': str(total_matches_lost),
            'Win Percentage': "{0:.2f}".format(win_percent * 100) + '%'
        }
        embed = discord.Embed(color=0x1ABC9C)
        embed.set_author(name=nickname, icon_url=avatar_url, url=avatar_url)
        for unit in data:
            embed.add_field(name=unit, value=data[unit])
        await message.channel.send(None, embed=embed)

    except Exception as e:
        cmd.log.error(e)
        await message.channel.send('Something went wrong or the user was not found.')
