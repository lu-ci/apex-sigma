from config import permitted_id
from sigma.core.permission import check_admin


def check_black(db, message):
    black_channel = False
    black_user = False
    server_is_black = False
    black = False
    if message.guild:
        if check_admin(message.author, message.channel):
            black = False
        channel_blacklist = db.get_settings(message.guild.id, 'BlacklistedChannels')
        if not channel_blacklist:
            channel_blacklist = []
        user_blacklist = db.get_settings(message.guild.id, 'BlacklistedUsers')
        if not user_blacklist:
            user_blacklist = []
        if message.author.id in user_blacklist:
            black_user = True
        if message.channel.id in channel_blacklist:
            black_channel = True
        server_is_black = db.get_settings(message.guild.id, 'IsBlacklisted')
    if message.author.id not in permitted_id:
        if black_channel or black_user or server_is_black:
            black = True
    return black


def check_overwrites(perms, author, channel, roles, cmd_name=None, mdl_name=None):
    overwritten = False
    if cmd_name:
        broad_exceptions = perms['CommandExceptions']
        trgt = cmd_name
    elif mdl_name:
        broad_exceptions = perms['ModuleExceptions']
        trgt = mdl_name
    else:
        trgt = None
        broad_exceptions = None
    if broad_exceptions:
        if trgt in broad_exceptions:
            exceptions = broad_exceptions[trgt]
            if author.id in exceptions['Users']:
                overwritten = True
            elif channel.id in exceptions['Channels']:
                overwritten = True
            for role in roles:
                if role.id in exceptions['Roles']:
                    overwritten = True
                    break
    return overwritten


def check_perms(db, message, command):
    if message.guild:
        if not check_admin(message.author, message.channel) or message.author.id not in permitted_id:
            perms = db.find_one('Permissions', {'ServerID': message.guild.id})
            if not perms:
                permitted = True
            else:
                cmd = command.name
                mdl = command.plugin.categories[0]
                ath = message.author
                chn = message.channel
                rls = message.author.roles
                if mdl in perms['DisabledModules']:
                    if check_overwrites(perms, ath, chn, rls, True):
                        permitted = True
                    else:
                        permitted = False
                elif cmd in perms['DisabledCommands']:
                    if check_overwrites(perms, ath, chn, rls, False):
                        permitted = True
                    else:
                        permitted = False
                else:
                    permitted = True
        else:
            permitted = True
    else:
        permitted = True
    return permitted
