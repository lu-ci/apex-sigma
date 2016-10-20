#!/usr/bin/env python3
import sys

import sigma

from config import Token as token
from config import StartupType, dsc_email, dsc_password

if __name__ == '__main__':
    client = sigma.Sigma()

    if StartupType == '0':
        if token == '':
            sys.exit('Token not provided, please open config.py and place your token.')
        else:
            pass
        try:
            client.run(token)
        except Exception as err:
            print(err)
    elif StartupType == '1':
        if dsc_email == '' or dsc_password == '':
            sys.exit('Discord Email and/or Passoword not provided, please open config.py and fill in those details.')
        else:
            pass
        try:
            client.run(dsc_email, dsc_password)
        except Exception as err:
            print(err)
    else:
        print('Failed loading connection settings.\nCheck your StartupType and make sure it\'s either 0 or 1.')
        sys.exit('Startup Type is not found.')
