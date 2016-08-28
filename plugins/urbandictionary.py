from plugin import Plugin
from config import cmd_ud
from config import MashapeKey as mashape_key
import requests
from utils import create_logger

class UrbanDictionary(Plugin):
    is_global = True
    log = create_logger(cmd_ud)

    async def on_message(self, message, pfx):
    # Urban Dictionary API
        if message.content.startswith(pfx + cmd_ud + ' '):
            await self.client.send_typing(message.channel)
            cmd_name = 'Urban Dictionary'
            ud_input = (str(message.content[len(cmd_ud) + 1 + len(pfx):]))
            url = "https://mashape-community-urban-dictionary.p.mashape.com/define?term=" + ud_input
            headers = {'X-Mashape-Key': mashape_key, 'Accept': 'text/plain'}
            # r = requests.get(url, headers=headers)
            # r_dec = r.read.decode('utf-8')
            response = requests.get(url, headers=headers).json()
            result_type = str((response['result_type']))
            if result_type == 'exact':
                try:
                    definition = str((response['list'][0]['definition']))
                    # permalink = str((response['list'][0]['permalink']))
                    # thumbs_up = str((response['list'][0]['thumbs_up']))
                    # thumbs_down = str((response['list'][0]['thumbs_down']))
                    example = str((response['list'][0]['example']))
                    await self.client.send_message(message.channel, 'Word: `' + ud_input + '`\n'
                                                                                      'Definition:\n```' + definition + '```\n' +
                                              'Example:\n```' + example + '\n```')
                    #print('CMD [' + cmd_name + '] > ' + initiator_data)
                except IndexError:
                    await self.client.send_message(message.channel, 'Something went wrong... The API dun goofed...')
                    #print('CMD [' + cmd_name + '] > ' + initiator_data)
            elif result_type == 'no_results':
                try:
                    await self.client.send_message(message.channel, 'No results :cry:')
                    #print('CMD [' + cmd_name + '] > ' + initiator_data)
                except:
                    await self.client.send_message(message.channel, 'Something went wrong, and we don\'t know what!')
                    #print('CMD [' + cmd_name + '] > ' + initiator_data)