import os
from io import BytesIO
import aiohttp
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


# Overwatch API
async def overwatch(cmd, message, args):
    ow_region_x = args[0]
    ow_name = ' '.join(args[1:]).replace('#', '-')
    ow_region = ow_region_x.lower().replace('na', 'us')

    if ow_region == 'us' or 'eu':
        try:
            profile = f'https://api.auroraproject.xyz/api/v1/overwatch?region={ow_region}&platform=pc&tag={ow_name}'
            async with aiohttp.ClientSession() as session:
                async with session.get(profile) as data:
                    profile_json = await data.json()
            avatar_link = profile_json['data']['player']['avatar']
            border_link = profile_json['data']['player']['border']
            try:
                tier_link = profile_json['data']['player']['tier']
            except:
                tier_link = None
            async with aiohttp.ClientSession() as session:
                async with session.get(avatar_link) as data:
                    avatar = await data.read()
            async with aiohttp.ClientSession() as session:
                async with session.get(border_link) as data:
                    border = await data.read()
            base = Image.open(cmd.resource('img/base.png'))
            overlay = Image.open(cmd.resource('img/overlay.png'))
            foreground = Image.open(BytesIO(border))
            foreground_res = foreground.resize((128, 128), Image.ANTIALIAS)
            background = Image.open(BytesIO(avatar))
            background_res = background.resize((72, 72), Image.ANTIALIAS)
            try:
                rank_link = profile_json['data']['player']['rank']
                async with aiohttp.ClientSession() as session:
                    async with session.get(rank_link) as data:
                        rank = await data.read()
                rankimg = Image.open(BytesIO(rank))
                rankimg_res = rankimg.resize((64, 64), Image.ANTIALIAS)
            except:
                rankimg_res = None
            base.paste(background_res, (28, 28))
            base.paste(overlay, (0, 0), overlay)
            base.paste(foreground_res, (0, 0), foreground_res)
            try:
                base.paste(rankimg_res, (310, 32), rankimg_res)
            except:
                pass
            if tier_link:
                async with aiohttp.ClientSession() as session:
                    async with session.get(tier_link) as data:
                        tier_img = await data.read()
                        tier_img = Image.open(BytesIO(tier_img))
                        tier_img = tier_img.resize((128, 64), Image.ANTIALIAS)
                base.paste(tier_img, (0, 64), tier_img)
            font = ImageFont.truetype("big_noodle_titling_oblique.ttf", 48)
            imgdraw = ImageDraw.Draw(base)
            name = profile_json['data']['player']['name']
            imgdraw.text((130, 38), name, (255, 255, 255), font=font)
            base.save('cache/ow_profile_' + message.author.id + '.png')
            level = str(profile_json['data']['player']['level'])
            quick = profile_json['data']['career_stats']['quick_play']
            comp = profile_json['data']['career_stats']['competitive']
            qg_won = str(quick['game']['games_won'])
            qg_playtime = str(quick['game']['time_played'])
            try:
                cg_played = str(comp['game']['games_played'])
            except:
                cg_played = 'None'
            try:
                cg_won = str(comp['game']['games_played'])
            except:
                cg_won = 'None'
            try:
                cg_lost = str(comp['miscellaneous']['games_lost'])
            except:
                cg_lost = 'None'
            try:
                rank = str(profile_json['data']['player']['rank_pts'])
            except:
                rank = 'None'
            try:
                cg_playtime = str(comp['game']['time_played'])
            except:
                cg_playtime = 'None'
            overwatch_profile = ('```Name: ' + name +
                                 '\nLevel: ' + level +
                                 '\nQuick Games:' +
                                 '\n    - Won: ' + qg_won +
                                 '\nCompetitive Games:' +
                                 '\n    - Played: ' + cg_played +
                                 '\n    - Won: ' + cg_won +
                                 '\n    - Lost: ' + cg_lost +
                                 '\n    - Rank: ' + rank +
                                 '\nPlaytime:' +
                                 '\n    - Quick: ' + qg_playtime + ' Hours' +
                                 '\n    - Competitive: ' + cg_playtime + ' Hours' + '```')
            await cmd.bot.send_file(message.channel, 'cache/ow_profile_' + message.author.id + '.png')
            os.remove('cache/ow_profile_' + message.author.id + '.png')
            await cmd.bot.send_message(message.channel, overwatch_profile)
        except KeyError:
            await cmd.bot.send_message(message.channel,
                                       'Something went wrong.\nThe servers are most likely overloaded, please try again.')
    else:
        await cmd.bot.send_message(message.channel,
                                   'Invalid region: `' + ow_region.upper() + '`\nAccepted regions are `NA` or `US` and `EU`\nUsage: `' + cmd.prefix + 'overwatch' + 'region battletag#ID')
