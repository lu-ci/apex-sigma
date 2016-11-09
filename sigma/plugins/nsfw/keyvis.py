import random

from .visual_novels import key_vn_list


async def keyvis(cmd, message, args):
    choice = None

    if not args:
        choice = random.choice(list(key_vn_list.keys()))
    else:
        choice = [x.lower() for x in args][0]

    try:
        item = key_vn_list[choice]
    except KeyError:
        await cmd.bot.send_message(message.channel, 'Nothing found for {:s}...'.format(
            ', '.join(['`{:s}`'.format(x) for x in args])))
        return

    ran_image_number = random.randint(1, item[1])
    ran_number_length = len(str(ran_image_number))

    url_base = 'https://cgv.blicky.net'
    image_url = '{:s}/{:s}/{:s}{:d}.jpg'.format(
            url_base, item[0], '0000'[:-ran_number_length], ran_image_number)

    await cmd.bot.send_message(message.channel, image_url)
