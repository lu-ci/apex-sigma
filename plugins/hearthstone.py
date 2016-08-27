from plugin import Plugin
from config import cmd_hearthstone
from config import MashapeKey as mashape_key
import requests


class Hearthstone(Plugin):
    is_global = True

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_hearthstone + ' '):
            await self.client.send_typing(message.channel)
            hs_input = (str(message.content[len(cmd_hearthstone) + 1 + len(pfx):]))
            url = "https://omgvamp-hearthstone-v1.p.mashape.com/cards/search/" + hs_input
            headers = {'X-Mashape-Key': mashape_key, 'Accept': 'text/plain'}
            response = requests.get(url, headers=headers).json()
            try:
                name = str(response[0]['name'])
                cardset = str(response[0]['cardSet'])
                rarity = str(response[0]['rarity'])
                cd_type = str(response[0]['type'])
                try:
                    cost = str(response[0]['cost'])
                except:
                    cost = '0'
                try:
                    faction = str(response[0]['faction'])
                except:
                    faction = 'None'
                try:
                    description = str(response[0]['flavor'])
                except:
                    description = 'None'
                if cd_type == 'Minion':
                    attack = str(response[0]['attack'])
                    health = str(response[0]['health'])
                    message_text = ('Name: `' + name + '`\n' +
                                    '\nType: `' + cd_type + '`' +
                                    '\nFaction: `' + faction + '`' +
                                    '\nRarity: `' + rarity + '`' +
                                    '\nCard Set: `' + cardset + '`' +
                                    '\nCost: `' + cost + '`' +
                                    '\nAttack: `' + attack + '`' +
                                    '\nHealth: `' + health + '`\n' +
                                    '\nDescription:```\n' + description + '```')
                elif cd_type == 'Spell':
                    try:
                        text = str(response[0]['text'])
                    except:
                        text = 'None'
                    message_text = ('Name: `' + name + '`\n' +
                                    '\nType: `' + cd_type + '`' +
                                    '\nFaction: `' + faction + '`' +
                                    '\nRarity: `' + rarity + '`' +
                                    '\nCard Set: `' + cardset + '`' +
                                    '\nCost: `' + cost + '`' +
                                    '\nText: \n```' + text + '\n```' +
                                    '\nDescription:```\n' + description + '```')
                elif cd_type == 'Weapon':
                    attack = str(response[0]['attack'])
                    durability = str(response[0]['durability'])
                    try:
                        text = str(response[0]['text'])
                    except:
                        text = 'None'
                    message_text = ('Name: `' + name + '`\n' +
                                    '\nType: `' + cd_type + '`' +
                                    '\nFaction: `' + faction + '`' +
                                    '\nRarity: `' + rarity + '`' +
                                    '\nCard Set: `' + cardset + '`' +
                                    '\nCost: `' + cost + '`' +
                                    '\nAttack: `' + attack + '`' +
                                    '\nDurability: `' + durability + '`' +
                                    '\nText: `' + text + '`' +
                                    '\nDescription:```\n' + description + '```')
                else:
                    message_text = 'Data incomplete or special, uncollectable card...'
                await self.client.send_message(message.channel, message_text)
                #print('CMD [' + cmd_name + '] > ' + initiator_data)
            except:
                try:
                    error = str(response['error'])
                    err_message = str(response['message'])
                    await self.client.send_message(message.channel, 'Error: ' + error + '. ' + err_message)
                except:
                    await self.client.send_message(message.channel, 'Something went wrong...')
                #print('CMD [' + cmd_name + '] > ' + initiator_data)