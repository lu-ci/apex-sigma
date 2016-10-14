import logging
from config import permitted_id, permitted_roles


def create_logger(name):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    file_handler = logging.FileHandler('log.txt')
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def italics(text):
    return '*' + text + '*'


def bold(text):
    return '**' + text + '**'


def bold_italics(text):
    return '***' + text + '***'


def strikeout(text):
    return '~~' + text + '~~'


def underline(text):
    return '__' + text + '__'


def underline_italics(text):
    return '__*' + text + '*__'


def underline_bold(text):
    return '__**' + text + '**__'


def underline_bold_italics(text):
    return '__***' + text + '***__'


def code(text):
    return '`' + text + '`'


def multilinecode(text):
    return '```' + text + '```'


def checkPermissions(user):
    # Checking a list of permitted users
    # if user.id in permitted_id: return True
    for id in permitted_id:
        if id == user.id:
            return True

    # Checking a list of permitted roles
    for permitted_role in permitted_roles:
        for user_role in user.roles:
            if user_role.name == permitted_role:
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
