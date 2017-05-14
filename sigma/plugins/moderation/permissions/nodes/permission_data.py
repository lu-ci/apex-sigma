def generate_default_data(message):
    perm_data = {
        'ServerID': message.guild.id,
        'DisabledCommands': [],
        'DisabledModules': [],
        'CommandExceptions': {},
        'ModuleExceptions': {},
    }
    return perm_data


def generate_cmd_data(cmd_name):
    generic_data = {
        'Users': [],
        'Channels': [],
        'Roles': []
    }
    return {cmd_name: generic_data}


def get_all_perms(db, message):
    perms = db.find_one('Permissions', {'ServerID': message.guild.id})
    if not perms:
        perms = generate_default_data(message)
        db.insert_one('Permissions', perms)
    return perms
