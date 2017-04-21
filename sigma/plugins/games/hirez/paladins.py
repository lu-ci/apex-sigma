import discord
import aiohttp
from .hirez_api import get_session, make_signature, paladins_base_url, make_timestamp
from config import HiRezDevID


async def paladins(cmd, message, args):
    if not args:
        return
    username = ' '.join(args)
    session_id = await get_session()
    hr_ts = make_timestamp()
    signature = make_signature('getplayer')
    data_url = paladins_base_url + 'getplayerJson/' + HiRezDevID + '/' + signature + '/' + session_id + '/' + hr_ts + '/' + username
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
    pals_general_stats = ('```yaml\nName: ' + player_name +
                          '\nRegion: ' + region +
                          '\nLevel: ' + str(level) +
                          '\nMastery: ' + str(mastery) +
                          '\nTeam: \"' + team + '\"' +
                          '\nStatus: \"' + status + '\"' +
                          '\nWon: ' + str(wins) +
                          '\nLost: ' + str(losses) +
                          '\nLeft: ' + str(leaves) +
                          '\nAchievements: ' + str(achis) +
                          '\nWorshipers: ' + str(worshs) +
                          '\n```')
    embed = discord.Embed(color=0x335183)
    embed.set_author(name=player_name, icon_url=avatar, url=avatar)
    embed.add_field(name='General Statistics', value=pals_general_stats, inline=False)
    await message.channel.send(None, embed=embed)
