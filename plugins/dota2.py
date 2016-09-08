from plugin import Plugin
from config import cmd_dota2
from config import SteamAPI
from utils import create_logger
import dota2api

class Dota2(Plugin):
    is_global = True
    log = create_logger(cmd_dota2)

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_dota2 + ' '):
            await self.client.send_typing(message.channel)
            cmd_name = 'Weather'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            d2_input = message.content[len(pfx) + len(cmd_dota2) + 1:]
            d2a = dota2api.Initialise(SteamAPI)
            history = d2a.get_match_history(account_id=d2_input)
            print(history)
            details = d2a.get_match_details(match_id = history['matches'][0]['match_id'])
            print(details)