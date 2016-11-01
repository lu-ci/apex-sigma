import os
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


def get_rank_info(level, location=174):
    if level == 60:
        return ('発明', location, '_en', (0, 204, 255))
    elif level >= 51:
        return ('現実', location, '_re', (0, 153, 255))
    elif level >= 41:
        return ('天堂', location, '_par', (0, 102, 255))
    elif level >= 31:
        return ('地獄', location, '_he', (51, 102, 255))
    elif level >= 21:
        return ('死', 184, '_de', (102, 102, 255))
    elif level >= 11:
        return ('苦', 184, '_pai', (153, 102, 255))
    else:
        return ('快', 184, '_pl', (204, 51, 255))


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
        out += 'Radicals: {:d}/{:d} ({:.2f}%) | Kanji: {:d}/{:d} ({:.2f}%)\n'.format(
            rad_cur, rad_total, (rad_cur / rad_total) * 100,
            kan_cur, kan_total, (kan_cur / kan_total) * 100)

        out += 'Your Next Review: "{:s}"\n'.format(
            parse_date(user['reviews']['next_date']))

        out += 'Lesson Queue: {:d} | Review Queue: {:d}\n'.format(
            user['lessons']['now'],
            user['reviews']['now'])

        out += 'Reviews Next Hour: {:d} | Reviews Next Day: {:d}\n'.format(
            user['reviews']['next_hour'],
            user['reviews']['next_day'])

    await cmd.reply('```json\n{:s}\n```'.format(out))


async def draw_image(cmd, message, user):
    rank_category, kanji_loc, ov_color, txt_color = get_rank_info(user['level'])

    img_type = 'big' if user['method'] == 'api' else 'small'

    # load images and fonts
    try:
        # TODO: use default avatar image if it could not be downloaded
        ava = Image.open(BytesIO(user['avatar'][1]))
        base = Image.open(
            cmd.resource('img/base_wk_{:s}.png'.format(img_type)))
        overlay = Image.open(
            cmd.resource('img/overlay_wk_{:s}{:s}.png'.format(img_type, ov_color)))
    except IOError as e:
        cmd.log.error('{:s}'.format(str(e)))
        raise e

    try:
        main_font = 'NotoSansCJKjp-Medium.otf'
        japanese_font = 'NotoSansCJKjp-Medium.otf'
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

    base.paste(ava, (15, 5))
    base.paste(overlay, (0, 0), overlay)

    review_color = (255, 255, 255)
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
                 (255, 255, 255), font=font3)

    if user['method'] == 'api':
        imgdraw.text((11, 88), 'Next Review: {:s}'.format(
            parse_date(user['reviews']['next_date'])),
            (255, 255, 255), font=font2)

        if int(user['reviews']['now']) > 150:
            review_color = (255, 174, 35)
            review_font = font1
            review_pos = (420, 108)

        imgdraw.text((11, 110), 'Next Hour: {:d}'.format(
            user['reviews']['next_hour']), (255, 255, 255), font=font4)
        imgdraw.text((136, 110), 'Next Day: {:d}'.format(
            user['reviews']['next_day']), (255, 255, 255), font=font4)

        imgdraw.text((252, 88), 'Radical: {:d}/{:d}'.format(
            user['radicals']['current'],
            user['radicals']['total']),
            (255, 255, 255), font=font2)

        imgdraw.text((363, 88), 'Kanji: {:d}/{:d}'.format(
            user['kanji']['current'],
            user['kanji']['total']),
            (255, 255, 255), font=font2)

        imgdraw.text((252, 110), 'Lessons: {:d}'.format(
            user['lessons']['now']), (255, 255, 255), font=font2)
        imgdraw.text((363, 110), 'Reviews: ', (255, 255, 255), font=font2)
        imgdraw.text(review_pos, str(user['reviews'][
                     'now']), review_color, font=review_font)

    tmp_file = 'cache/ani/wk_{:s}.png'.format(message.author.id)
    base.save(tmp_file)
    await cmd.reply_file(tmp_file)
    os.remove(tmp_file)
