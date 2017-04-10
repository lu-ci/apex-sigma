import random
import imgurpython

from config import ImgurClientID, ImgurClientSecret


async def imgur(cmd, message, args):
    if not args:
        return
    q = ' '.join(args)
    imgur_client = imgurpython.ImgurClient(ImgurClientID, ImgurClientSecret)
    gallery_items = imgur_client.gallery_search(q, advanced=None, sort='time', window='all', page=0)
    chosen_item = random.choice(gallery_items).link
    await message.channel.send(chosen_item)
