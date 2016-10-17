import requests

from sigma.plugin import Plugin
from sigma.utils import create_logger

from config import MashapeKey as mashape_key


class UrbanDictionary(Plugin):
    is_global = True
    log = create_logger('ud')

    async def on_message(self, message, pfx):
    # Urban Dictionary API
        if message.content.startswith(pfx + 'ud' + ' '):
            await self.client.send_typing(message.channel)
            cmd_name = 'Urban Dictionary'
            ud_input = str(message.content[len('ud') + 1 + len(pfx):])
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            entry = ud_input[-2:]
            if entry.strip().isnumeric():
                ud_input = ud_input[:-2] #stripping entry from the term
                if int(entry) > 10:
                    await self.client.send_message(message.channel, 'Out of boundary, please select a number from `1` to `10`')
                    return
                entry = int(entry) - 1 #converting the entry number
            else: entry = 0

            url = "https://mashape-community-urban-dictionary.p.mashape.com/define?term=" + ud_input
            headers = {'X-Mashape-Key': mashape_key, 'Accept': 'text/plain'}
            response = requests.get(url, headers=headers).json()
            result_type = str((response['result_type']))
            if result_type == 'exact':
                try:
                    definition = str((response['list'][entry]['definition']))
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
