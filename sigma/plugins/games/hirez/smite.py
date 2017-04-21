import discord
import aiohttp
from humanfriendly.tables import format_pretty_table as boop
from .hirez_api import get_session, make_signature, smite_base_url, make_timestamp
from config import HiRezDevID


async def smite(cmd, message, args):
    if not args:
        return
    username = ' '.join(args)
    session_id = await get_session()
    hr_ts = make_timestamp()
    signature = make_signature('getplayer')
    data_url = smite_base_url + 'getplayerJson/' + HiRezDevID + '/' + signature + '/' + session_id + '/' + hr_ts + '/' + username
    async with aiohttp.ClientSession() as session:
        async with session.get(data_url) as data:
            data = await data.json()
    if len(data) == 0:
        embed = discord.Embed(color=0xDB0000, title='❗ Player ' + username + ' was not found.')
        await message.channel.send(None, embed=embed)
        return
    data = data[0]
    avatar = message.author.default_avatar_url
    if 'Avatar_URL' in data:
        avatar = data['Avatar_URL']
    player_name = data['Name']
    region = data['Region']
    status = data['Personal_Status_Message']
    level = data['Level']
    leaves = data['Leaves']
    wins = data['Wins']
    losses = data['Losses']
    mastery = data['MasteryLevel']
    team = data['Team_Name']
    achis = data['Total_Achievements']
    worshs = data['Total_Worshippers']
    smite_general_stats = ('```yaml\nName: ' + player_name +
                           '\nRegion: ' + region +
                           '\nLevel: ' + str(level) +
                           '\nMastery: ' + str(mastery) +
                           '\nTeam: \"' + team + '\"' +
                           '\nStatus: \"' + status + '\"' +
                           '\nTotal:' +
                           '\n  - Won: ' + str(wins) +
                           '\n  - Lost: ' + str(losses) +
                           '\n  - Left: ' + str(leaves) +
                           '\n  - Achievements: ' + str(achis) +
                           '\n  - Worshipers: ' + str(worshs) +
                           '\n```')
    ranked_inices = ['RankedConquest', 'RankedDuel', 'RankedJoust']
    ranked_table_head = ['']
    ranked_wins_row = ['Won']
    ranked_losses_row = ['Lost']
    ranked_leaves_row = ['Left']
    ranked_points_row = ['Points']
    ranked_tier_row = ['Tier']

    for item in ranked_inices:
        rank_data = data[item]
        ranked_table_head.append(rank_data['Name'])
        ranked_wins_row.append(rank_data['Wins'])
        ranked_losses_row.append(rank_data['Losses'])
        ranked_leaves_row.append(rank_data['Leaves'])
        ranked_points_row.append(rank_data['Points'])
        ranked_tier_row.append(rank_data['Tier'])
    ranked_table_raw = [ranked_table_head, ranked_wins_row, ranked_losses_row, ranked_leaves_row, ranked_points_row, ranked_tier_row]
    pretty_rank = boop(ranked_table_raw)
    smite_ranked_stats = ('```haskell\n' + pretty_rank + '\n```')
    embed = discord.Embed(color=0xffce00)
    embed.set_author(name=player_name, icon_url=avatar, url=avatar)
    embed.add_field(name='General Statistics', value=smite_general_stats, inline=False)
    embed.add_field(name='Ranked Statistics', value=smite_ranked_stats, inline=False)
    await message.channel.send(None, embed=embed)
