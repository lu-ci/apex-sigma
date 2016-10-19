from .database import DatabaseError


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
