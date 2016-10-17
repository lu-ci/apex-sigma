from plugin import Plugin
from utils import create_logger
import requests
from PIL import Image
from io import BytesIO
import os


class MagicTheGathering(Plugin):

    is_global = True
    log = create_logger('mtg')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'mtg '):
            await self.client.send_typing(message.channel)
            q = message.content[len(pfx) + len('mtg') + 1:]
            cards = requests.get('https://api.magicthegathering.io/v1/cards?name=' + str(q)).json()
            n = 0
            list_text = 'List of cards found for `' + str(q) + '`:\n```'
            if len(cards['cards']) > 1:
                for entry in cards['cards']:
                    n += 1
                    list_text += '\n#' + str(n) + ' ' + entry['name']
                try:
                    await self.client.send_message(message.channel,
                                                   list_text + '\n```\nPlease type the number corresponding to the card of your choice `(1 - ' + str(
                                                       len(cards)) + ')`')
                except:
                    await self.client.send_message(message.channel,
                                                   'The list is way too big, please be more specific...')
                    return
                choice = await self.client.wait_for_message(author=message.author, channel=message.channel, timeout=20)
                await self.client.send_typing(message.channel)
                try:
                    card_no = int(choice.content) - 1
                except:
                    await self.client.send_message(message.channel, 'Not a number or timed out... Please start over')
                    return
                if choice is None:
                    return
            else:
                card_no = 0
            try:
                card_img_url = cards['cards'][card_no]['imageUrl']
                card_img_request = requests.get(card_img_url).content
                card_img = Image.open(BytesIO(card_img_request))
                card_img.save('cache/mtg_' + message.author.id + '.png')
                await self.client.send_file(message.channel, 'cache/mtg_' + message.author.id + '.png')
                os.remove('cache/mtg_' + message.author.id + '.png')
            except Exception as err:
                print(err)
                await self.client.send_message(message.channel, 'Something went wrong...')
