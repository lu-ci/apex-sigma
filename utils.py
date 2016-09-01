import logging


def create_logger(name):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    file_handler = logging.FileHandler('log.txt')
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def italics(text):
    return '*' + text + '*'


def bold(text):
    return '**' + text + '**'


def bold_italics(text):
    return '***' + text + '***'


def strikeout(text):
    return '~~' + text + '~~'


def underline(text):
    return '__' + text + '__'


def underline_italics(text):
    return '__*' + text + '*__'


def underline_bold(text):
    return '__**' + text + '**__'


def underline_bold_italics(text):
    return '__***' + text + '***__'


def code(text):
    return '`' + text + '`'


def multilinecode(text):
    return '```' + text + '```'