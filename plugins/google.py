from plugin import Plugin
from utils import create_logger
import googleapiclient

class Google(Plugin):

    is_global = True
    log = create_logger('google')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'google'):
            