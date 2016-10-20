def italics(text):
    return '*{:s}*'.format(text)


def bold(text):
    return '**{:s}**'.format(text)


def strikeout(text):
    return '~~{:s}~~'.format(text)


def underline(text):
    return '__{:s}__'.format(text)


def code(text):
    return '`{:s}`'.format(text)


def codeblock(text, syntax=''):
    return '```{:s}\n{:s}\n```'.format(syntax, text)
