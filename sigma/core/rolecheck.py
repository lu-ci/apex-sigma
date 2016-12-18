def matching_role(server, role_name):
    match = None
    for role in server.roles:
        if role.name.lower() == role_name.lower():
            match = role
            break
    return match


def user_matching_role(user, role_name):
    match = None
    for role in user.roles:
        if role.name.lower() == role_name.lower():
            match = role
            break
    return match
