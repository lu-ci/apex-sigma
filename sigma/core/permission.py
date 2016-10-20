from .database import DatabaseError, IntegrityError


def check_channel_nsfw(db, channel_id):
    try:
        query = 'SELECT PERMITTED FROM NSFW WHERE CHANNEL_ID=?'
        results = db.execute(query, channel_id)
        perms = results.fetchone()

        if perms and perms[0] == 'Yes':
            return True
        else:
            return False
    except DatabaseError:
        return False


def set_channel_nsfw(db, channel_id):
    success = False

    try:
        query = "INSERT INTO NSFW (CHANNEL_ID, PERMITTED) VALUES (?, ?)"
        db.execute(query, channel_id, 'Yes')
        db.commit()
        success = True
    except IntegrityError:
        query = "DELETE from NSFW where CHANNEL_ID=?;"
        db.execute(query, channel_id)
        db.commit()

    return success


def check_admin(user, channel):
    return user.permissions_in(channel).administrator
