import requests

from sigma.plugin import Plugin
from sigma.utils import create_logger

from config import ITADKey


class ITAD(Plugin):
    is_global = True
    log = create_logger('itad')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'itad'):
            await self.client.send_typing(message.channel)
            cmd_name = 'IsThereAnyDeal'
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            request = requests.get('https://api.isthereanydeal.com/v01/deals/list/eu2/?key=' + ITADKey + '&country=RS&offset=0&limit=20').json()
            try:
                deal_text = 'Latest 10 Deals:\n```'
                currency = request['.meta']['currency']
                for i in range(0, 10):
                    game_title = request['data']['list'][i]['title']
                    shop_name = request['data']['list'][i]['shop']['name']
                    price_old = str(request['data']['list'][i]['price_old'])
                    price_new = str(request['data']['list'][i]['price_new'])
                    price_cut = str(request['data']['list'][i]['price_cut'])
                    deal_text += '\n#' + str(i+1) + ': ' + game_title + ' on ' + shop_name + ' for ' + price_new + currency + '/' + price_old + ' (' + price_cut + '%)'
                deal_text += '\n```'
                print(deal_text)
                await self.client.send_message(message.channel, deal_text)
            except:
                await self.client.send_message(message.channel, 'We seem to have ran into an error.')
