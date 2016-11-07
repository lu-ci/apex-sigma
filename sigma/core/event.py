from sigma.core.formatting import code, codeblock

from .callable import Callable
from .callable import NotEnabledError


class Event(Callable):
    def __init__(self, plugin, info):
        try:
            super().__init__(plugin, info)
        except NotEnabledError:
            return

        self.type = info['type']

    def help(self):
        usage = self.usage
        return 'Usage: {:s}\n{:s}'.format(
                code(usage), codeblock(self.desc))
