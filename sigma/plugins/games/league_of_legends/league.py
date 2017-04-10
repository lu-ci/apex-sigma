import os
import aiohttp
from io import BytesIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from config import RiotAPIKey


# League of Legends API
async def league(cmd, message, args):
    lol_input = ' '.join(args)

    try:
        region, smnr_name = lol_input.lower().split(maxsplit=1)
    except Exception as e:
        cmd.log.error(e)
        await message.channel.send(str(e))
        return

    smnr_name_table = smnr_name.replace(' ', '')
    smnr_by_name_url = 'https://' + region + '.api.pvp.net/api/lol/' + region + '/v1.4/summoner/by-name/' + smnr_name + '?api_key=' + RiotAPIKey
    version_url = 'https://global.api.pvp.net/api/lol/static-data/' + region + '/v1.2/versions?api_key=' + RiotAPIKey
    async with aiohttp.ClientSession() as session:
        async with session.get(version_url) as data:
            version_json = await data.json()
    version = str(version_json[0])

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(smnr_by_name_url) as data:
                smnr_by_name = await data.json()
        smnr_id = str(smnr_by_name[smnr_name_table]['id'])
        smnr_icon = str(smnr_by_name[smnr_name_table]['profileIconId'])
        icon_url = 'http://ddragon.leagueoflegends.com/cdn/' + version + '/img/profileicon/' + smnr_icon + '.png'
        smnr_lvl = str(smnr_by_name[smnr_name_table]['summonerLevel'])
        summary_url = 'https://' + region + '.api.pvp.net/api/lol/' + region + '/v1.3/stats/by-summoner/' + smnr_id + '/summary?season=SEASON2016&api_key=' + RiotAPIKey
        async with aiohttp.ClientSession() as session:
            async with session.get(summary_url) as data:
                summary = await data.json()
        league_url = 'https://' + region + '.api.pvp.net/api/lol/' + region + '/v2.5/league/by-summoner/' + smnr_id + '?api_key=' + RiotAPIKey
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(league_url) as data:
                    league_data = await data.json()
            league_name = league_data[smnr_id][0]['name']
            league_tier = league_data[smnr_id][0]['tier']
        except:
            league_name = 'No League'
            league_tier = 'No Rank'
        # Image Start
        async with aiohttp.ClientSession() as session:
            async with session.get(icon_url) as data:
                avatar = await data.read()
        base = Image.open(cmd.resource('img/base.png'))
        overlay = Image.open(cmd.resource('img/overlay_lol.png'))
        background = Image.open(BytesIO(avatar))
        background_res = background.resize((72, 72), Image.ANTIALIAS)
        foreground = Image.open(cmd.resource('img/border_lol.png'))
        foreground_res = foreground.resize((64, 64), Image.ANTIALIAS)
        base.paste(background_res, (28, 28))
        base.paste(overlay, (0, 0), overlay)
        base.paste(foreground_res, (32, 32), foreground_res)
        fontfile = cmd.resource("fonts/big_noodle_titling_oblique.ttf")
        font = ImageFont.truetype(fontfile, 32)
        font2 = ImageFont.truetype(fontfile, 16)
        font3 = ImageFont.truetype(fontfile, 48)
        imgdraw = ImageDraw.Draw(base)
        imgdraw.text((130, 38), smnr_name, (255, 255, 255), font=font)
        imgdraw.text((130, 70), league_name + ' - ' + league_tier, (255, 255, 255), font=font2)
        imgdraw.text((326, 38), smnr_lvl, (255, 255, 255), font=font3)
        base.save('cache/lol_profile_' + message.author.id + '.png')
        # Image End

        try:
            item = next(
                (item for item in summary['playerStatSummaries'] if item['playerStatSummaryType'] == 'RankedSolo5x5'),
                None)
            if item:
                ranked = item
                ranked_wins = str(ranked['wins'])
                ranked_losses = str(ranked['losses'])
                ranked_kills = str(ranked['aggregatedStats']['totalChampionKills'])
                ranked_minions = str(ranked['aggregatedStats']['totalMinionKills'])
                ranked_turrets = str(ranked['aggregatedStats']['totalTurretsKilled'])
                ranked_neutrals = str(ranked['aggregatedStats']['totalNeutralMinionsKilled'])
                ranked_assists = str(ranked['aggregatedStats']['totalAssists'])
                ranked_text = ('Wins: ' + ranked_wins +
                               '\nLosses: ' + ranked_losses +
                               '\nKills: ' + ranked_kills +
                               '\nAssists: ' + ranked_assists +
                               '\nMinion Kills: ' + ranked_minions +
                               '\nTurret Kills: ' + ranked_turrets +
                               '\nJungle Minion Kills: ' + ranked_neutrals)
            else:
                ranked_text = 'None'
        except:
            ranked_text = 'None'
        try:
            item = next(
                (item for item in summary['playerStatSummaries'] if item['playerStatSummaryType'] == 'Unranked'), None)
            if item:
                normal = item
                normal_wins = str(normal['wins'])
                normal_kills = str(normal['aggregatedStats']['totalChampionKills'])
                normal_minions = str(normal['aggregatedStats']['totalMinionKills'])
                normal_turrets = str(normal['aggregatedStats']['totalTurretsKilled'])
                normal_neutrals = str(normal['aggregatedStats']['totalNeutralMinionsKilled'])
                normal_assists = str(normal['aggregatedStats']['totalAssists'])
                normal_text = ('Wins: ' + normal_wins +
                               '\nKills: ' + normal_kills +
                               '\nAssists: ' + normal_assists +
                               '\nMinion Kills: ' + normal_minions +
                               '\nTurret Kills: ' + normal_turrets +
                               '\nJungle Minion Kills: ' + normal_neutrals)
            else:
                normal_text = 'None'
        except SyntaxError:
            normal_text = 'None'
        if ranked_text == 'None' and normal_text == 'None':
            await message.channel.send('No stats found.')
        else:
            await message.channel.send_file('cache/lol_profile_' + message.author.id + '.png')
            os.remove('cache/lol_profile_' + message.author.id + '.png')
            await cmd.bot.send_message(message.channel,
                                       'Normal Stats:\n```' + normal_text + '\n```\nRanked Stats:\n```' + ranked_text + '\n```')
    # except Exception as e:
    except SyntaxError:
        # `cmd.log.error(e)
        await message.channel.send('Something went wrong, PANIC!')
