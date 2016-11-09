import os
import requests
from io import BytesIO
from PIL import Image

from config import MashapeKey


async def hearthstone(cmd, message, args):
    hs_input = ' '.join(args)

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
                await cmd.bot.send_message(message.channel, card_list + '\n```\nPlease type the number corresponding to the card of your choice `(1 - ' + str(
                                                   len(response)) + ')`')
                choice = await cmd.bot.wait_for_message(author=message.author, channel=message.channel, timeout=20)

                try:
                    card_no = int(choice.content) - 1
                except:
                    await cmd.bot.send_message(message.channel, 'Not a number or timed out... Please start over')
                    return

                if choice is None:
                    return
            except:
                await cmd.bot.send_message(message.channel, 'The list is way too big, please be more specific...')
                return
        else:
            card_no = 0
    except:
        try:
            error = str(response['error'])
            err_message = str(response['message'])
            await cmd.bot.send_message(message.channel, 'Error: ' + error + '.\n' + err_message)
            return
        except Exception as e:
            cmd.log.error(e)
            await cmd.bot.send_message(message.channel, 'Something went wrong...')
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

        await cmd.bot.send_file(message.channel, 'cache/hs_' + message.author.id + '.png')
        os.remove('cache/hs_' + message.author.id + '.png')

        if flavor_text == '':
            return
        else:
            flavor_out = '```\n' + flavor_text + '\n```'
            await cmd.bot.send_message(message.channel, flavor_out)
    except:
        try:
            error = str(response['error'])
            err_message = str(response['message'])
            await cmd.bot.send_message(message.channel, 'Error: ' + error + '.\n' + err_message)
        except Exception as e:
            cmd.log.error(e)
            await cmd.bot.send_message(message.channel, 'Something went wrong...')
