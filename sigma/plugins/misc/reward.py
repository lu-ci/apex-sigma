import random

from sigma.plugin import Plugin
from sigma.utils import create_logger


class RewardOnMessage(Plugin):
    is_global = True
    log = create_logger('Add Point For Activity')

    async def on_message(self, message, pfx):
        if message.server is not None:
            query = "SELECT EXISTS (SELECT LVL, LV_CHECK, POINTS FROM POINT_SYSTEM WHERE USER_ID=?);"
            info_grabber_checker = self.db.execute(query, str(message.author.id))

            for info_check in info_grabber_checker:
                if info_check[0] == 0:
                    query = "INSERT INTO POINT_SYSTEM (USER_ID, LVL, LV_CHECK, POINTS) VALUES (?, ?, ?, ?)"
                    self.db.execute(query, str(message.author.id), 0, 0, 0)
                    self.db.commit()
                else:
                    query = "SELECT LVL, LV_CHECK, POINTS FROM POINT_SYSTEM WHERE USER_ID=?"
                    number_grabber = self.db.execute(query, str(message.author.id))
                    points = 0
                    level = 0
                    level_check = 0
                    for number in number_grabber:
                        level = number[0]
                        level_check = number[1]
                        points = number[2]

                    points_old = points
                    points_new = points_old + random.randint(1, 10)
                    level_point = format(points_new / (601 + (69 * int(level))), ".0f")
                    level_should = int(level_point)

                    query = "UPDATE POINT_SYSTEM SET POINTS=? WHERE USER_ID=?"
                    self.db.execute(query, str(points_new), str(message.author.id))

                    if level_should > level_check:
                        query = "UPDATE POINT_SYSTEM SET LVL=? WHERE USER_ID=?"
                        self.db.execute(query, str(level_should), str(message.author.id))

                        query = "UPDATE POINT_SYSTEM SET LV_CHECK=? WHERE USER_ID=?"
                        self.db.execute(query, str(level_should), str(message.author.id))
                    else:
                        break

                    self.db.commit()
