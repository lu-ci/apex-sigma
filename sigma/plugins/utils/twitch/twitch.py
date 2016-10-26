from twitch.api import v3 as api
from config import TwitchClientID
# uncomment these for PIL
# from PIL import Image
# from PIL import ImageFont
# from PIL import ImageDraw
# import requests
# from io import BytesIO
# import os


async def twitch(cmd, message, args):
    try:
        # data collection
        if TwitchClientID != '':
            twitch.CLIENTID = TwitchClientID

        twitch_input = ' '.join(args)

        channel = api.channels.by_name(twitch_input)
        name = channel['display_name']
        # will be the last or current game streamer is playing.
        game = channel['game']
        avatar_url = channel['logo']
        followers = channel['followers']
        steam = api.streams.by_channel(twitch_input)['stream']
        if isinstance(steam, None):
            online = False
        else:
            start = steam['created_at']
            online = True

        # data End; pillow start?
        if online:
            await cmd.reply('display name: ' + name +
                            '\nNow playing: ' + game +
                            '\nAvatar: ' + avatar_url +
                            '\nfollowers: ' + str(followers) +
                            '\nstream started at ' + start)
        else:
            await cmd.reply('display name: ' + name +
                            '\nllast seen playing: ' + game +
                            '\nAvatar: ' + avatar_url +
                            '\nfollowers: ' + str(followers))
        # TODO: impliment PIL into this module
        # avatar_raw = requests.get(avatar_url).content
        #
        #        with Image.open(BytesIO(avatar_raw)) as avatar:
        #            base = Image.open(cmd.resource('img/base.png'))
        #            overlay = Image.open(cmd.resource('img/overlay.png'))
        #            base.paste(avatar, (0,0))
        #
    except Exception as e:
        cmd.log.error(e)
        await cmd.reply('An unknown error occurred.\nError: ' + str(e))
