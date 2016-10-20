import logging


def create_logger(name):
    fmt = '%(asctime)s %(name)-15s %(levelname)-8s %(message)s'
    formatter = logging.Formatter(fmt)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    file_handler = logging.FileHandler('log.txt')
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(file_handler)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger
