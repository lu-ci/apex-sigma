import random
import imgurpython

from config import ImgurClientID, ImgurClientSecret


async def imgur(cmd, message, args):
    q = ' '.join(args)
    try:
        imgur_client = imgurpython.ImgurClient(ImgurClientID, ImgurClientSecret)
    except imgurpython.helpers.error.ImgurClientError:
        cmd.log.error('Imgur ClientID + ClientSecret')
        return

    gallery_items = imgur_client.gallery_search(q, advanced=None, sort='time', window='all', page=0)

    try:
        chosen_item = random.choice(gallery_items).link
    except Exception as e:
        cmd.log.error(e)
        await cmd.bot.send_message(message.channel, 'No results...')
        return

    await cmd.bot.send_message(message.channel, chosen_item)
