import os
import discord
import datetime
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from io import BytesIO


def parse_date(time, fmt='%B %d, %Y %H:%M'):
    if time:
        return datetime.datetime.fromtimestamp(time).strftime(fmt)
    else:
        return 'Unknown'


def get_rank_info(level, location=174, color=(27, 111, 95)):
    if level == 60:
        return '発明', location, '_en', color
    elif level >= 51:
        return '現実', location, '_re', color
    elif level >= 41:
        return '天堂', location, '_par', color
    elif level >= 31:
        return '地獄', location, '_he', color
    elif level >= 21:
        return '死', 184, '_de', color
    elif level >= 11:
        return '苦', 184, '_pai', color
    else:
        return '快', 184, '_pl', color


async def text_message(cmd, message, user):
    srs = user['srs']

    out = ''
    out += '"{:s}" of Sect "{:s}"\n'.format(user['name'], user['title'])
    out += 'Level {:d} Apprentice\n'.format(user['level'])
    out += 'Scribed {:d} topics & {:d} posts\n'.format(
        user['forums']['topics'], user['forums']['posts'])

    out += 'Serving the Crabigator since "{:s}"\n'.format(
        parse_date(user['creation_date']))

    out += 'Apprentice: {:d} | Guru: {:d} | Master {:d} | Enlightened {:d} | Burned {:d}\n'.format(
        srs['apprentice'], srs['guru'], srs['master'], srs['enlightened'], srs['burned'])

    # we have additional information through the api
    if user['method'] == 'api':
        rad_cur = user['radicals']['current']
        rad_total = user['radicals']['total']
        kan_cur = user['kanji']['current']
        kan_total = user['kanji']['total']

        rad_percentage = ''
        if rad_total:
            rad_percentage = '({:.2f}%) '.format((rad_cur / rad_total) * 100)

        kan_percentage = ''
        if kan_total:
            kan_percentage = '({:.2f}%) '.format((kan_cur / kan_total) * 100)

        out += 'Radicals: {:d}/{:d} {:}| Kanji: {:d}/{:d} {:}\n'.format(
            rad_cur, rad_total, rad_percentage,
            kan_cur, kan_total, kan_percentage)

        out += 'Your Next Review: "{:s}"\n'.format(
            parse_date(user['reviews']['next_date']))

        out += 'Lesson Queue: {:d} | Review Queue: {:d}\n'.format(
            user['lessons']['now'],
            user['reviews']['now'])

        out += 'Reviews Next Hour: {:d} | Reviews Next Day: {:d}\n'.format(
            user['reviews']['next_hour'],
            user['reviews']['next_day'])

    await message.channel.send('```json\n{:s}\n```'.format(out))


async def draw_image(cmd, message, user, clr):
    user_color = clr
    dark = False
    rank_color = (255, 255, 255)
    clr1 = int(user_color[:2], 16)
    clr2 = int(user_color[2:-2], 16)
    clr3 = int(user_color[4:], 16)
    clr_barier = 150
    barriered_count = 0
    clr_list = [clr1, clr2, clr3]
    for clr in clr_list:
        if clr > clr_barier:
            barriered_count += 1
    if barriered_count >= 2:
        dark = True
    transed_color = (clr1, clr2, clr3)
    rank_category, kanji_loc, ov_color, txt_color = get_rank_info(user['level'], color=transed_color)
    img_type = 'big' if user['method'] == 'api' else 'small'
    if img_type == 'big':
        base_size = (450, 132)
    else:
        base_size = (450, 87)
    color_base_size = (450, 87)

    # load images and fonts
    try:
        ava_raw = Image.open(BytesIO(user['avatar'][1]))
        ava = ava_raw.resize((78, 78), Image.ANTIALIAS)
        base = Image.new('RGBA', base_size, (0, 0, 0, 0))
        color_base = Image.new('RGB', color_base_size, transed_color)
        if dark:
            rank_color = (38, 38, 38)
            overlay = Image.open(
                cmd.resource('img/overlay_wk_{:s}_dark.png'.format(img_type)))
        else:
            overlay = Image.open(
                cmd.resource('img/overlay_wk_{:s}.png'.format(img_type)))
    except IOError as e:
        cmd.log.error('{:s}'.format(str(e)))
        raise e

    try:
        main_font = cmd.resource('fonts/NotoSansCJKjp-Medium.otf')
        japanese_font = cmd.resource('fonts/NotoSansCJKjp-Medium.otf')
        font1 = ImageFont.truetype(main_font, 15)
        font2 = ImageFont.truetype(main_font, 13)
        font3 = ImageFont.truetype(japanese_font, 21)
        font4 = ImageFont.truetype(main_font, 12)
    except OSError as e:
        cmd.log.error('{:s}'.format(str(e)))
        cmd.log.error('You\'re missing the fonts!')
        raise e

    try:
        imgdraw = ImageDraw.Draw(base)
    except IOError as e:
        cmd.log.error('{:s}'.format(str(e)))
        raise e

    base.paste(color_base, (9, 0))
    base.paste(ava, (15, 5))
    base.paste(overlay, (0, 0), overlay)

    review_color = txt_color
    review_font = font2
    review_pos = (420, 110)

    imgdraw.text((95, 2), '{:s} of sect {:s}'.format(
        user['name'], user['title']), txt_color, font=font1)
    imgdraw.text((116, 31), str(
        user['srs']['apprentice']), txt_color, font=font2)
    imgdraw.text((182, 31), str(
        user['srs']['guru']), txt_color, font=font2)
    imgdraw.text((248, 31), str(
        user['srs']['master']), txt_color, font=font2)
    imgdraw.text((314, 31), str(
        user['srs']['enlightened']), txt_color, font=font2)
    imgdraw.text((380, 31), str(
        user['srs']['burned']), txt_color, font=font2)
    imgdraw.text((95, 60), 'Level: {:d}'.format(
        user['level']), txt_color, font=font2)

    imgdraw.text((250, 60), 'Joined: {:s}'.format(
        parse_date(user['creation_date'], fmt='%B %d, %Y')),
                 txt_color, font=font2)

    imgdraw.text((kanji_loc, 52), rank_category,
                 rank_color, font=font3)

    if user['method'] == 'api':
        imgdraw.text((11, 88), 'Next Review: {:s}'.format(
            parse_date(user['reviews']['next_date'])),
                     txt_color, font=font2)

        if int(user['reviews']['now']) > 150:
            review_color = (255, 0, 0)
            review_font = font2

        imgdraw.text((11, 110), 'Next Hour: {:d}'.format(
            user['reviews']['next_hour']), txt_color, font=font4)
        imgdraw.text((136, 110), 'Next Day: {:d}'.format(
            user['reviews']['next_day']), txt_color, font=font4)

        imgdraw.text((252, 88), 'Radical: {:d}/{:d}'.format(
            user['radicals']['current'],
            user['radicals']['total']),
                     txt_color, font=font2)

        imgdraw.text((363, 88), 'Kanji: {:d}/{:d}'.format(
            user['kanji']['current'],
            user['kanji']['total']),
                     txt_color, font=font2)

        imgdraw.text((252, 110), 'Lessons: {:d}'.format(
            user['lessons']['now']), txt_color, font=font2)
        imgdraw.text((363, 110), 'Reviews: ', txt_color, font=font2)
        imgdraw.text(review_pos, str(user['reviews'][
                                         'now']), review_color, font=review_font)

    tmp_file = f'cache/wk_{message.author.id}.png'
    base.save(tmp_file)
    await message.channel.send(file=discord.File(tmp_file))
    os.remove(tmp_file)
