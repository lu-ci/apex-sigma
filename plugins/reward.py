from plugin import Plugin
from utils import create_logger
import sqlite3
import random


class RewardOnMessage(Plugin):
    is_global = True
    log = create_logger('Add Point For Activity')

    async def on_message(self, message, pfx):
        dbsql = sqlite3.connect('storage/server_settings.sqlite', timeout=20)
        if message.server is not None:
            info_grabber_checker = dbsql.execute(
                "SELECT EXISTS (SELECT LVL, LV_CHECK, POINTS FROM POINT_SYSTEM WHERE USER_ID=?);",
                (str(message.author.id),))
            for info_check in info_grabber_checker:
                if info_check[0] == 0:
                    #print('Non-Existant: Inserting')
                    dbsql.execute("INSERT INTO POINT_SYSTEM (USER_ID, LVL, LV_CHECK, POINTS) VALUES (?, ?, ?, ?)",
                                  (str(message.author.id), 0, 0, 0,))
                    dbsql.commit()
                else:
                    number_grabber = dbsql.execute("SELECT LVL, LV_CHECK, POINTS FROM POINT_SYSTEM WHERE USER_ID=?",
                                                   (str(message.author.id),))
                    for number in number_grabber:
                        level_check = number[1]
                        points = number[2]
                    points_old = points
                    points_new = points_old + random.randint(1, 10)
                    level_point = format(points_new / 500, ".0f")
                    level_should = int(level_point)
                    # print('Existant: Updating points to: ' + str(points_new) + ' from ' + str(
                    # points_old) + '\nLevel should be: ' + str(level_should) + ' / ' + str(level_check))
                    dbsql.execute("UPDATE POINT_SYSTEM SET POINTS= ? WHERE USER_ID= ?",
                                  (str(points_new), str(message.author.id),))
                    dbsql.commit()
                    if level_should > level_check:
                        dbsql.execute("UPDATE POINT_SYSTEM SET LVL= ? WHERE USER_ID= ?",
                                      (str(level_should), str(message.author.id),))
                        dbsql.execute("UPDATE POINT_SYSTEM SET LV_CHECK= ? WHERE USER_ID= ?",
                                      (str(level_should), str(message.author.id),))
                        dbsql.commit()
                        await self.client.send_message(message.channel,
                                                       'Congratulations <@' + message.author.id + '>!\nYou just leveled up to **Level ' + str(
                                                           level_point) + '**!')
                    else:
                        return
        else:
            await self.client.send_message(message.channel, 'I don\'t recommend using me in Private Messaging.')


class LevelCheck(Plugin):
    is_global = True
    log = create_logger('Level Check')

    async def on_message(self, message, pfx):
        dbsql = sqlite3.connect('storage/server_settings.sqlite', timeout=20)
        if message.content.startswith(pfx + 'level'):
            cmd_name = 'Level Check'
            try:
                self.log.info(
                    'User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                    message.author,
                    message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            try:
                user_id = message.mentions[0].id
                mid_msg = ' is'
                end_msg = 'has'
            except:
                user_id = message.author.id
                mid_msg = '. You are'
                end_msg = 'have'
            number_grabber = dbsql.execute("SELECT LVL, LV_CHECK, POINTS FROM POINT_SYSTEM WHERE USER_ID=?",
                                           (str(user_id),))
            for number in number_grabber:
                level = number[0]
                points = number[2]
            await self.client.send_message(message.channel, 'Okay, <@' + user_id + '>' + mid_msg + ' **Level ' + str(
                level) + '** and currently ' + end_msg + ' **' + str(points) + ' Points**!')
