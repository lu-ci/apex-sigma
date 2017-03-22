from config import permitted_id
from sigma.core.permission import check_admin


def check_black(db, message):
    black_channel = False
    black_user = False
    server_is_black = False
    black = False
    if message.server:
        if check_admin(message.author, message.channel):
            black = False
        channel_blacklist = db.get_settings(message.server.id, 'BlacklistedChannels')
        if not channel_blacklist:
            channel_blacklist = []
        user_blacklist = db.get_settings(message.server.id, 'BlacklistedUsers')
        if not user_blacklist:
            user_blacklist = []
        if message.author.id in user_blacklist:
            black_user = True
        if message.channel.id in channel_blacklist:
            black_channel = True
        server_is_black = db.get_settings(message.server.id, 'IsBlacklisted')
    if message.author.id not in permitted_id:
        if black_channel or black_user or server_is_black:
            black = True
    return black
