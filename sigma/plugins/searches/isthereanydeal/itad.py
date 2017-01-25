import discord
import requests

from config import ITADKey


async def itad(cmd, message, args):
    request = requests.get(
        'https://api.isthereanydeal.com/v01/deals/list/eu2/?key=' + ITADKey + '&country=RS&offset=0&limit=20').json()
    currency = request['.meta']['currency']
    embed = discord.Embed(color=0x1abc9c, title='💰 Latest Game Deals')
    for i in range(0, 3):
        game_title = request['data']['list'][i]['title']
        shop_name = request['data']['list'][i]['shop']['name']
        price_old = str(request['data']['list'][i]['price_old'])
        price_new = str(request['data']['list'][i]['price_new'])
        price_cut = str(request['data']['list'][i]['price_cut'])
        embed.add_field(name='Game Title and Shop',
                        value='```yaml\n\"' + game_title + '\" on \"' + shop_name + '\"```', inline=False)
        embed.add_field(name='Deal Price', value='```ruby\n' + price_new + ' ' + currency + '\n```', inline=True)
        embed.add_field(name='Default Price', value='```ruby\n' + price_old + ' ' + currency + '\n```', inline=True)
        embed.add_field(name='Price Cut', value='```ruby\n' + price_cut + ' ' + currency + '\n```', inline=True)

    await cmd.bot.send_message(message.channel, None, embed=embed)
