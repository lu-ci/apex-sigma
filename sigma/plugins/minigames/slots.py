import random
import time
from config import permitted_id


async def slots(cmd, message, args):
    current_timestamp = int(time.time())
    cooldown_finder_data = {
        'Type': 'Slots',
        'UserID': message.author.id,
        'ServerID': message.server.id
    }
    cooldown_insert_data = {
        'Type': 'Slots',
        'UserID': message.author.id,
        'ServerID': message.server.id,
        'LastTimestamp': current_timestamp
    }
    cooldown_data = cmd.db.find('Cooldowns', cooldown_finder_data)
    n = 0
    last_use = 0
    for result in cooldown_data:
        n += 1
        try:
            last_use = result['LastTimestamp']
        except:
            last_use = 0
    if n == 0:
        off_cooldown = True
        not_in_db = True
    else:
        not_in_db = False
        if current_timestamp > last_use + 20:
            off_cooldown = True
        else:
            off_cooldown = False

    if off_cooldown:
        if not_in_db:
            cmd.db.insert_one('Cooldowns', cooldown_insert_data)
        else:
            updatetarget = {"UserID": message.author.id, "ServerID": message.server.id, "Type": "Slots"}
            updatedata = {"$set": {"LastTimestamp": current_timestamp}}
            cmd.db.update_one('Cooldowns', updatetarget, updatedata)
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
        if curr_pts < 50:
            await cmd.bot.send_message(message.channel,
                                       'I\'m sorry <@' + message.author.id + '>. I\'m afraid I can\'t let you do that.\nYou don\'t have enough points.')
            return
        symbols = [':sunny:', ':crescent_moon:', ':eggplant:', ':gun:', ':diamond_shape_with_a_dot_inside:', ':bell:',
                   ':maple_leaf:', ':musical_note:', ':gem:', ':fleur_de_lis:', ':trident:', ':knife:', ':fire:',
                   ':clown:', ':radioactive:', ':green_heart:', ':telephone:', ':hamburger:', ':banana:',
                   ':tumbler_glass:']
        res_1 = random.choice(symbols)
        res_2 = random.choice(symbols)
        res_3 = random.choice(symbols)

        slot_view = ':arrow_forward: ' + res_1 + ' ' + res_2 + ' ' + res_3 + ' :arrow_backward:'

        if res_1 == res_2 == res_3:
            win = True
            pts = 10000
            three_notify = 'The user **' + message.author.name + '** on **' + message.server.name + '** has just won ' + str(
                pts) + ' on Slots!'
            for user in cmd.bot.get_all_members():
                if user.id == permitted_id[0]:
                    await cmd.bot.send_message(user, three_notify)
                    break
        elif res_1 == res_2 or res_1 == res_3 or res_2 == res_3:
            win = True
            pts = 200
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
            new_pts = curr_pts - 50
            updatetarget = {"UserID": message.author.id, "ServerID": message.server.id}
            updatedata = {"$set": {"Points": new_pts}}
            cmd.db.update_one(collection, updatetarget, updatedata)
            results = 'Sorry, you didn\'t win anything this time...'
        out = slot_view + '\n\n' + results
        await cmd.bot.send_message(message.channel, out)
    else:
        timeout = (last_use + 20) - current_timestamp
        await cmd.bot.send_message(message.channel,
                                   'You need to wait another ' + str(timeout) + ' seconds before using that again.')
