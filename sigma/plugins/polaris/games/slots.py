import random


async def slots(cmd, message, args):
    symbols = [':sunny:', ':crescent_moon:', ':eggplant:', ':gun:', ':diamond_shape_with_a_dot_inside:', ':bell:',
               ':maple_leaf:', ':musical_note:', ':gem:', ':fleur_de_lis:', ':trident:', ':knife:', ':fire:',
               ':clown:', ':radioactive:', ':green_heart:', ':telephone:', ':hamburger:', ':banana:']
    res_1 = random.choice(symbols)
    res_2 = random.choice(symbols)
    res_3 = random.choice(symbols)

    slot_view = ':arrow_forward: ' + res_1 + ' ' + res_2 + ' ' + res_3 + ' :arrow_backward:'

    if res_1 == res_2 == res_3:
        win = True
        pts = 5000
    elif res_1 == res_2 or res_1 == res_3 or res_2 == res_3:
        win = True
        pts = 10
    else:
        win = False
        pts = 0
    if win:
        target = None
        collection = 'PointSystem'
        finddata = {
            'UserID': message.author.id,
            'ServerID': message.server.id
        }
        finddata_results = cmd.db.find(collection, finddata)
        for item in finddata_results:
            target = item
        curr_pts = target['Points']
        add_pts = pts
        new_pts = curr_pts + add_pts
        updatetarget = {"UserID": message.author.id, "ServerID": message.server.id}
        updatedata = {"$set": {"Points": new_pts}}
        cmd.db.update_one(collection, updatetarget, updatedata)
        results = 'You\'ve been awarded ' + str(pts) + ' points.'
    else:
        results = 'Sorry, you didn\'t win anything this time...'
    out = slot_view + '\n\n' + results
    await cmd.bot.send_message(message.channel, out)
