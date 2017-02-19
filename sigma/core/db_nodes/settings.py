def generate_defaults(server):
    default_settings = {
        'ServerID': server.id,
        'Greet': True,
        'GreetMessage': 'Hello %user_mention%, welcome to %server_name%',
        'GreetChannel': server.default_channel.id,
        'GreetPM': False,
        'Bye': True,
        'ByeMessage': '%user_mention% has left the server.',
        'ByeChannel': server.default_channel.id,
        'CleverBot': True,
        'Unflip': False,
        'ShopEnabled': True,
        'ShopItems': [],
        'RandomEvents': False,
        'EventChance': 1,
        'ChatAnalysis': False,
        'MarkovCollect': False,
        'BlockInvites': False,
        'AntiSpam': False,
        'IsBlacklisted': False,
        'BlacklistedChannels': [],
        'BlacklistedUsers': [],
        'AutoRole': None,
        'SelfRoles': [],
        'LoggingEnabled': False,
        'WarnedUsers': {},
        'WarnLimit': 2
    }
    return default_settings


def add_new_server_settings_node(db, server):
    search = db['ServerSettings'].find({'ServerID': server.id})
    n = len(list(search))
    if n == 0:
        default_settings = generate_defaults(server)
        db['ServerSettings'].insert_one(default_settings)


def init_server_settings_node(db, servers):
    for server in servers:
        add_new_server_settings_node(db, server)


def get_settings_node(db, server_id, setting):
    collection = 'ServerSettings'
    finddata = {
        'ServerID': server_id,
    }
    search = db[collection].find_one(finddata)
    if search:
        return search[setting]
    else:
        return None


def set_settings_node(db, server_id, setting, setting_variable):
    collection = 'ServerSettings'
    updatetarget = {'ServerID': server_id}
    updatedata = {'$set': {setting: setting_variable}}
    db[collection].update_one(updatetarget, updatedata)


def check_for_missing_settings_node(db, server):
    default = generate_defaults(server)
    for key in default:
        try:
            get_settings_node(db, server.id, key)
        except:
            value = default[key]
            set_settings_node(db, server.id, key, value)
