from plugin import Plugin
from config import MashapeKey
import requests
from utils import create_logger
from PIL import Image
from io import BytesIO
import os

class Hearthstone(Plugin):
    is_global = True
    log = create_logger('hearthstone')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'hearthstone' + ' '):
            await self.client.send_typing(message.channel)
            cmd_name = 'Hearthstone'
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            hs_input = (str(message.content[len('hearthstone') + 1 + len(pfx):]))
            url = 'https://omgvamp-hearthstone-v1.p.mashape.com/cards/search/' + hs_input + '?locale=enUS'
            headers = {'X-Mashape-Key': MashapeKey, 'Accept': 'text/plain'}
            response = requests.get(url, headers=headers).json()
            card_list = '```'
            try:
                if len(response) > 1:
                    n = 0
                    for card in response:
                        n += 1
                        card_list += ('\n#' + str(n) + ': ' + card['name'])
                    try:
                        await self.client.send_message(message.channel,
                                                       card_list + '\n```\nPlease type the number corresponding to the card of your choice `(1 - ' + str(
                                                           len(response)) + ')`')
                        choice = await self.client.wait_for_message(author=message.author, channel=message.channel, timeout=20)
                        await self.client.send_typing(message.channel)
                        try:
                            card_no = int(choice.content) - 1
                        except:
                            await self.client.send_message(message.channel,
                                                           'Not a number or timed out... Please start over')
                            return
                        if choice is None:
                            return
                    except:
                        await self.client.send_message(message.channel,
                                                       'The list is way too big, please be more specific...')
                        return
                else:
                    card_no = 0
            except:
                try:
                    error = str(response['error'])
                    err_message = str(response['message'])
                    await self.client.send_message(message.channel, 'Error: ' + error + '.\n' + err_message)
                    return
                except:
                    await self.client.send_message(message.channel, 'Something went wrong...')
                    return
            try:
                card_img_url = response[card_no]['img']
                card_img_request = requests.get(card_img_url).content
                card_img = Image.open(BytesIO(card_img_request))
                card_img.save('cache/hs_' + message.author.id + '.png')
                try:
                    flavor_text = response[card_no]['flavor']
                except:
                    flavor_text = ''
                await self.client.send_file(message.channel, 'cache/hs_' + message.author.id + '.png')
                os.remove('cache/hs_' + message.author.id + '.png')
                if flavor_text == '':
                    return
                else:
                    flavor_out = '```\n' + flavor_text + '\n```'
                    await self.client.send_message(message.channel, flavor_out)
            except:
                try:
                    error = str(response['error'])
                    err_message = str(response['message'])
                    await self.client.send_message(message.channel, 'Error: ' + error + '.\n' + err_message)
                except:
                    await self.client.send_message(message.channel, 'Something went wrong...')
