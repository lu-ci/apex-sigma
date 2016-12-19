import requests
import discord

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
                selector = await cmd.bot.send_message(message.channel, card_list + '\n```\nPlease type the number corresponding to the card of your choice `(1 - ' + str(
                                                   len(response)) + ')`')
                choice = await cmd.bot.wait_for_message(author=message.author, channel=message.channel, timeout=20)
                await cmd.bot.delete_message(selector)
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
        card_name = response[card_no]['name']
        card_img_url = response[card_no]['img']
        embed = discord.Embed(title=card_name,color=0x1ABC9C)
        embed.set_image(url=card_img_url)

        try:
            flavor_text = response[card_no]['flavor']
        except:
            flavor_text = None
        if flavor_text:
            flavor_out = '```\n' + flavor_text + '\n```'
            embed.add_field(name='Info', value=flavor_out)
        await cmd.bot.send_message(message.channel, None, embed=embed)
    except:
        try:
            error = str(response['error'])
            err_message = str(response['message'])
            await cmd.bot.send_message(message.channel, 'Error: ' + error + '.\n' + err_message)
        except Exception as e:
            cmd.log.error(e)
            await cmd.bot.send_message(message.channel, 'Something went wrong...')
