import requests

from config import ITADKey


async def itad(cmd, message, args):
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
            deal_text += '\n#' + str(i + 1) + ': ' + game_title + ' on ' + shop_name + ' for ' + price_new + currency + '/' + price_old + ' (' + price_cut + '%)'

        deal_text += '\n```'
        await cmd.reply(deal_text)
    except Exception as e:
        cmd.log.error(e)
        await cmd.reply('We seem to have ran into an error.')
