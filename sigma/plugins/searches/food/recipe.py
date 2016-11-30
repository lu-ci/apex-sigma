import requests
from config import Food2ForkAPIKey


async def recipe(cmd, message, args):
    if not args:
        await cmd.bot.send_message(message.channel, cmd.help())
        return
    else:
        search = ' '.join(args)
    try:
        url = 'http://food2fork.com/api/search?key=' + Food2ForkAPIKey + '&q=' + search
        search_data = requests.get(url).json()
    except Exception as e:
        cmd.log.error(e)
        await cmd.bot.send_message(message.channel, 'I was unable to parse the page of the results.')
        return
    try:
        count = search_data['count']
    except Exception as e:
        cmd.log.error(e)
        await cmd.bot.send_message(message.channel, 'I was unable to parse the page of the results.')
        return
    if count == 0:
        await cmd.bot.send_message(message.channel, 'No results were found for that, sorry.')
        return
    else:
        info = search_data['recipes'][0]
        title = info['title']
        source = info['publisher']
        source_url = info['source_url']
        image_url = info['image_url']
        out = '**' + title + '** found on **' + source + '**\nRecipe: <' + source_url + '>\n\nImage: ' + image_url
        await cmd.bot.send_message(message.channel, out)
