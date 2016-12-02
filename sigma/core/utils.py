from config import permitted_id


def checkPermissions(user):
    # Checking a list of permitted users
    # if user.id in permitted_id: return True
    for id in permitted_id:
        if id == user.id:
            return True

    return False


def getArguments(raw, separator):
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
