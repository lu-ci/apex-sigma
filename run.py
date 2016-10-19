#!/usr/bin/env python3
import sys
import os

from sigma.core import Sigma

from config import Token as token
from config import StartupType, dsc_email, dsc_password


if __name__ == '__main__':

    if not os.path.isfile('config.py'):
        sys.exit(
            'Fatal Error: config.py is not present.\nIf you didn\'t already, rename config_example.py to config.py, fill out your credentials and try again.')
    else:
        print('config.py present, continuing...')

    client = Sigma()

    if StartupType == '0':
        if token == '':
            sys.exit('Token not provided, please open config.py and place your token.')

        try:
            client.run(token)
        except Exception as e:
            client.log.error(e)

    elif StartupType == '1':
        if dsc_email == '' or dsc_password == '':
            sys.exit('Discord Email and/or Passoword not provided, please open config.py and fill in those details.')

        try:
            client.run(dsc_email, dsc_password)
        except Exception as err:
            client.log.error(err)
    else:
        client.log.error('Failed loading connection settings.\nCheck your StartupType and make sure it\'s either 0 or 1.')
        sys.exit('Startup Type is not found.')
