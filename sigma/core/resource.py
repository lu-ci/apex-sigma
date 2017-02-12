from config import AppRoot
from os import path

global_resource_dir = path.join(AppRoot, 'res')


class ResourceLoadError(Exception):
    pass


def global_resource(res):
    resource = path.join(global_resource_dir, res)

    if path.exists(resource):
        return resource
    else:
        raise ResourceLoadError
