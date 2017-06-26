from .database import get_user_data, get_key
from .message import text_message, draw_image


async def wanikani(cmd, message, args):
    show_text = False

    if args and args[-1] == 'text':
        show_text = True
        args.pop()

    key, username = await get_key(cmd, message, args)

    user = await get_user_data(cmd, message, key, username)
    if user:
        if show_text:
            await text_message(cmd, message, user)
        else:
            try:
                if message.mentions:
                    clr = str(message.mentions[0].color)[1:]
                else:
                    clr = str(message.author.color)[1:]
                await draw_image(cmd, message, user, clr)
            except OSError:
                # failed to generate image
                await text_message(cmd, message, user)
