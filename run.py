#!/usr/bin/env python3
import os

from sigma.core import Sigma

from config import Token

if __name__ == '__main__':

    if not os.path.isfile('config.py'):
        print('Fatal Error: No config file!\nRename and edit the config_example.py before running Sigma!')
        exit(404)
    else:
        print('config.py present, continuing...')
    if not Token or Token == '':
        print('Token not provided, please open config.py and place your token.')
        exit(410)
    client = Sigma()
    client.run(Token)
