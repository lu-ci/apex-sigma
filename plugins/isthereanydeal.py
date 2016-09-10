from plugin import Plugin
from config import cmd_itad
from config import ITADKey as key
from utils import create_logger
import requests

class ITAD(Plugin):
    is_global = True
    log = create_logger(cmd_itad)

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_itad):
            await self.client.send_typing(message.channel)
            cmd_name = 'IsThereAnyDeal'
            self.log.info('\nUser %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            request = requests.get('https://api.isthereanydeal.com/v01/deals/list/eu2/?key=' + key + '&country=RS&offset=0&limit=20').json()
            try:
                deal_text = 'Latest 10 Deals:\n```'
                currency = request['.meta']['currency']
                for i in range(0, 10):
                    game_title = request['data']['list'][i]['title']
                    shop_name = request['data']['list'][i]['shop']['name']
                    shop_url = request['data']['list'][i]['urls']['buy']
                    price_old = str(request['data']['list'][i]['price_old'])
                    price_new = str(request['data']['list'][i]['price_new'])
                    price_cut = str(request['data']['list'][i]['price_cut'])
                    deal_text += '\n#' + str(i+1) + ': ' + game_title + ' on ' + shop_name + ' for ' + price_new + currency + '/' + price_old + ' (' + price_cut + '%)'
                deal_text += '\n```'
                print(deal_text)
                await self.client.send_message(message.channel, deal_text)
            except:
                await self.client.send_message(message.channel, 'We seem to have ran into an error.')