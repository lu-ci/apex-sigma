import os
import yaml
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
    user_ava += '.png'
    return user_ava


def load_module_list():
    directory = 'sigma/plugins'
    module_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'plugin.yml':
                file_path = (os.path.join(root, file))
                with open(file_path) as plugin_file:
                    plugin_data = yaml.safe_load(plugin_file)
                    try:
                        category = plugin_data['categories'][0]
                        if category.lower() not in module_list and category not in ['administration', 'special']:
                            module_list.append(category)
                    except:
                        pass
    return module_list


def convert_hms(hms):
    hrs, mns, secs = hms.split(':')
    out_time = (int(hrs) * 3600) + (int(mns) * 60) + int(secs)
    return out_time
