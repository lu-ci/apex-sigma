def role_exists(server, role_name):
    exists = False
    for role in server.roles:
        if role.name.lower() == role_name.lower():
            exists = True
    return exists


def matching_role(server, role_name):
    match = None
    for role in server.roles:
        if role.name.lower() == role_name.lower():
            match = role
            break
    return match
