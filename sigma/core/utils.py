from config import permitted_id


def check_owner(user):
    # Checking a list of permitted users
    # if user.id in permitted_id: return True
    return bool(user.id in permitted_id)


def get_arguments(raw, separator):
    raw = raw.strip()
    args = raw.count(' ') + 1
    out = []

    for arg in range(0, args):
        if raw.find(separator) == -1:
            out.append(raw)
            return tuple(out)

        temp = raw[:raw.find(separator)]
        raw = raw[len(temp):].strip()
        out.append(temp)

    return tuple(out)


def split_list(alist, wanted_parts=1):
    length = len(alist)

    return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
            for i in range(wanted_parts)]


def user_avatar(user):
    if user.avatar_url != '':
        user_ava = '.'.join(user.avatar_url.split('.')[:-1])
    else:
        user_ava = user.default_avatar_url
    return user_ava

