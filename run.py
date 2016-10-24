#!/usr/bin/env python3
import sys
import os

from sigma.core import Sigma

from config import Token as token

if __name__ == '__main__':

    if not os.path.isfile('config.py'):
        sys.exit(
            'Fatal Error: config.py is not present.\nIf you didn\'t already, rename config_example.py to config.py, fill out your credentials and try again.')
    else:
        print('config.py present, continuing...')

    client = Sigma()

    if token == '':
        sys.exit('Token not provided, please open config.py and place your token.')
    try:
        client.run(token)
    except Exception as e:
        client.log.error(e)
