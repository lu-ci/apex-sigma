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
        total_kills = 0
        total_deaths = 0
        total_time_played = 0
        total_kills_knife = 0
        total_kills_headshot = 0
        total_shots_fired = 0
        total_shots_hit = 0
        total_rounds_played = 0
        total_mvps = 0
        total_matches_won = 0
        total_matches_played = 0

        for stat in stats:
            nam = stat[n]
            val = stat[v]
            if nam == 'total_kills':
                total_kills = val
            elif nam == 'total_deaths':
                total_deaths = val
            elif nam == 'total_time_played':
                total_time_played = val
            elif nam == 'total_kills_knife':
                total_kills_knife = val
            elif nam == 'total_kills_headshot':
                total_kills_headshot = val
            elif nam == 'total_shots_fired':
                total_shots_fired = val
            elif nam == 'total_shots_hit':
                total_shots_hit = val
            elif nam == 'total_rounds_played':
                total_rounds_played = val
            elif nam == 'total_mvps':
                total_mvps = val
            elif nam == 'total_matches_won':
                total_matches_won = val
            elif nam == 'total_matches_played':
                total_matches_played = val

        kdr = total_kills / total_deaths
        accuracy = total_shots_hit / total_shots_fired
        total_matches_lost = total_matches_played - total_matches_won
        win_percent = total_matches_won / total_matches_played

        data = {
            'Playtime': str(total_time_played // 3600) + ' Hours',
            'Kills': str(total_kills),
            'Deaths': str(total_deaths),
            'Kill/Death Ratio': "{0:.2f}".format(kdr),
            'Shots Fired': str(total_shots_fired),
            'Shots Hit': str(total_shots_hit),
            'Accuracy': "{0:.2f}".format(accuracy * 100) + '%',
            'Headshots': str(total_kills_headshot),
            'Knife Kills': str(total_kills_knife),
            'Rounds Played': str(total_rounds_played),
            'Total MVPs': str(total_mvps),
            'Matches Played': str(total_matches_played),
            'Matches Won': str(total_matches_won),
            'Matches Lost': str(total_matches_lost),
            'Win Percentage': "{0:.2f}".format(win_percent * 100) + '%'
        }
        embed = discord.Embed(color=0x1ABC9C)
        embed.set_author(name=nickname, icon_url=avatar_url, url=avatar_url)
        for unit in data:
            embed.add_field(name=unit, value=data[unit])
        await cmd.bot.send_message(message.channel, None, embed=embed)

    except Exception as e:
        cmd.log.error(e)
        await cmd.bot.send_message(message.channel, 'Something went wrong or the user was not found.')
