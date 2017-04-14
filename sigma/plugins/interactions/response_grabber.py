import yaml
import random


def grab_response(file, trigger):
    with open(file) as resp_file:
        data = yaml.safe_load(resp_file)
        resp = random.choice(data[trigger])
    return resp
