import os
from time import time
from datetime import datetime
import logging
import coloredlogs


log_fmt = '%(levelname)-6s %(asctime)s %(name)-20s %(message)s'
log_dir = 'log'

if not os.path.exists(log_dir):
    os.mkdir(log_dir)

logfile_name = datetime.fromtimestamp(time()).strftime('%Y%m%d-%H%M%S') + '.log'
log_path = os.path.join(log_dir, logfile_name)
log_file = open(log_path, mode='a+')


def create_logger(name):
    logger = logging.getLogger(name)

    coloredlogs.install(level='INFO', fmt=log_fmt)
    coloredlogs.install(level='INFO', fmt=log_fmt, stream=log_file, isatty=False)

    return logger
