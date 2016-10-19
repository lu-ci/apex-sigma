from .database import get_user_data, get_key
from .message import text_message, draw_image


async def wanikani(bot, message, args):
    show_text = False
    args = message.content.split(' ')
    args.pop(0)

    if args and args[-1] == 'text':
        show_text = True
        args.pop()

    key, username = await get_key(bot, message, args)

    user = await get_user_data(bot, message, key, username)

    if user:
        if show_text:
            await text_message(bot, user)
        else:
            try:
                await draw_image(bot, message, user)
            except OSError:
                # failed to generate image
                await text_message(bot, message, user)
