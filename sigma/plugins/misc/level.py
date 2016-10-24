async def level(cmd, message, args):
    try:
        user_id = message.mentions[0].id
        mid_msg = ' is'
        end_msg = 'has'
    except:
        user_id = message.author.id
        mid_msg = '. You are'
        end_msg = 'have'

    query = 'SELECT LVL, LV_CHECK, POINTS FROM POINT_SYSTEM WHERE USER_ID=?'
    number_grabber = cmd.db.execute(query, str(user_id))
    cmd.db.commit()

    level = 0
    points = 0

    for number in number_grabber:
        level = number[0]
        points = number[2]

    msg = 'Okay, <@{:s}>{:s} **Level {:d}** and currently {:s} **{:d} Points**!'
    await cmd.reply(msg.format(user_id, mid_msg, level, end_msg, points))
