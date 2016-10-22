import logging
import coloredlogs


fmt = '%(asctime)s %(name)-25s %(levelname)-8s %(message)s'
formatter = coloredlogs.ColoredFormatter(fmt)

log_file = open('log.txt', mode='a+')


def create_logger(name):
    logger = logging.getLogger(name)

    coloredlogs.install(level='INFO', fmt=fmt)
    coloredlogs.install(level='INFO', fmt=fmt, stream=log_file, isatty=False)

    return logger
