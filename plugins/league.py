from plugin import Plugin
from commands import *
import random
import os
import wget

class LeagueOfLegends(Plugin):
    is_global = True

    async def on_message(self, message, pfx):
        # League of Legends API
        if message.content.startswith(pfx + cmd_league + ' '):
            await self.client.send_typing(message.channel)
            cmd_name = 'League of Legends'
            champ_no = ['266', '103', '84', '12', '32', '34', '1', '22', '136' '268', '432', '53', '63', '201', '51', '69',
                        '31', '42', '122', '131', '36', '119', '245', '60', '28', '81', '9', '114', '105', '3', '41', '86',
                        '150', '79', '104', '120', '74', '420', '39', '40', '59' '24', '126', '202', '222', '429', '43',
                        '30', '38', '55', '10', '85', '121', '203', '240', '96', '7', '64' '89', '127', '236', '117', '99',
                        '54', '90', '57', '11' '21' '82', '25', '267', '75', '111', '76', '56', '20', '2', '61', '80', '78',
                        '133', '33', '421', '58', '107', '92', '68', '13', '113', '35', '98', '102', '27', '14', '15', '72',
                        '37', '16', '50', '134', '223' '163', '91', '44', '17', '412', '0', '18', '48', '23', '4' '29',
                        '77', '6', '110', '67', '45', '161', '254', '112', '8', '106', '19', '62', '101', '5' '157', '83',
                        '154', '238', '115', '26', '143']
            skin_no = ['0', '1', '2']
            champ_back = random.choice(champ_no)
            skin_back = random.choice(skin_no)
            if os.path.isfile('lolsig.png'):
                os.remove('lolsig.png')
            lol_input = (str(message.content[len(cmd_league) + 1 + len(pfx):]))
            region_x, ignore, summoner_name_x = lol_input.partition(' ')
            summoner_name = summoner_name_x.lower()
            region = region_x.lower()
            lol_sig_url = (
                'http://lolsigs.com/' + summoner_name + '_' + region + '_' + champ_back + '_' + skin_back + '.png')
            wget.download(lol_sig_url)
            os.rename(summoner_name + '_' + region + '_' + champ_back + '_' + skin_back + '.png', 'lolsig.png')
            try:
                await self.client.send_file(message.channel, 'lolsig.png')
                if os.path.isfile('lolsig.png'):
                    os.remove('lolsig.png')
                #print('CMD [' + cmd_name + '] > ' + initiator_data)
            except KeyError:
                #print('CMD [' + cmd_name + '] > ' + initiator_data)
                await self.client.send_message(message.channel,
                                          'Something went wrong.\nThe servers are most likely overloaded, please try again.')